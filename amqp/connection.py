"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import asyncio
import os

import aioamqp
from sanic.log import logger

import settings
from amqp.consumers import example_consumer



class _Connect:

    def __init__(self, app, prefix, params):
        self.app = app
        self.prefix = prefix
        self.params = params

    @property
    def transport(self) -> str:
        return '{}_transport'.format(self.prefix)

    @property
    def protocol(self) -> str:
        return '{}_protocol'.format(self.prefix)

    @property
    def channel(self) -> str:
        return '{}_channel'.format(self.prefix)

    async def __call__(self, *args, **kwargs):
        transport, protocol = await aioamqp.connect(
            **self.params,
            on_error=_error_callback_factory(connect_func=self)
        )

        channel = await protocol.channel()
        if channel is None:
            logger.error(f'_Connect {self.channel} is None')

        setattr(self.app, self.transport, transport)
        setattr(self.app, self.protocol, protocol)
        setattr(self.app, self.channel, channel)

        logger.info('Successful AMQP connection "{}" for worker {}'.format(self.prefix, os.getpid()))


def _error_callback_factory(connect_func: _Connect):
    async def error_callback(exception):
        app = connect_func.app
        prefix = connect_func.prefix
        transport_prop = connect_func.transport
        protocol_prop = connect_func.protocol
        channel_prop = connect_func.channel

        transport = getattr(connect_func.app, transport_prop, None)
        protocol = getattr(connect_func.app, protocol_prop, None)
        channel = getattr(connect_func.app, channel_prop, None)

        # при нормальном закрытии channels происходит это исключение
        # if isinstance(exception, (aioamqp.ChannelClosed, aioamqp.AmqpClosedConnection)):
        logger.warning('error_callback_factory exception type {} channel {} func {} exception {}'.format(
            str(type(exception)), str(connect_func.channel), str(connect_func), str(exception)))

        # для одного соединения этот коллбек может быть вызван дважды
        # условие позволяет этого избежать
        # вот тут упомянуто об этом баге (https://github.com/Polyconseil/aioamqp/issues/65#issuecomment-301737344)
        if not all([transport, protocol, channel]):
            return

        setattr(app, transport_prop, None)
        setattr(app, protocol_prop, None)
        setattr(app, channel_prop, None)

        logger.warning('error_callback_factory AMQP connection "{}" is lost. Worker: {}'.format(prefix, os.getpid()))

        pending_count = 0

        while pending_count < settings.RECONNECT_RESTART_COUNT:
            try:
                logger.warning('error_callback_factory new_log AMQP connection "%s" attempt %s for worker %s',
                    prefix, pending_count, os.getpid())
                return await connect_func()
            except Exception:  # OSError, ConnectionTimeout
                logger.warning('error_callback_factory new_log AMQP connection "%s" attempt %s FAILED for worker %s, sleep...',
                    prefix, pending_count, os.getpid())

                pending_count += 1
                await asyncio.sleep(settings.RECONNECT_SLEEP_TIME)
        else:
            logger.error('error_callback_factory new_log AMQP connection %s attempts are UNSUCCESSFUL for worker %s', prefix, os.getpid())

    return error_callback


async def open_amqp_connections(app, config):
    connections = config['connections']

    for conn in connections:
        prefix = conn['prefix']
        params = conn['params']

        await _Connect(app, prefix, params)()


async def close_amqp_connections(app, config):
    connections = config['connections']

    for conn in connections:
        prefix = conn['prefix']

        transport_name = '{}_transport'.format(prefix)
        protocol_name = '{}_protocol'.format(prefix)

        transport = getattr(app, transport_name, None)
        protocol = getattr(app, protocol_name, None)

        if protocol:
            await protocol.close()

        if transport:
            transport.close()


async def bind_queue_for_channel(channel, queue_name, exchange_name, routing_key=None, arguments=None):
    await channel.queue_declare(queue_name, durable=True, arguments=arguments)
    if exchange_name:
        await channel.queue_bind(
            queue_name=queue_name,
            exchange_name=exchange_name,
            routing_key=routing_key if routing_key is not None else queue_name,
        )


async def consume_amqp(app, loop):
    await app.example_channel.exchange_declare(
        exchange_name=settings.EXAMPLE_EXCHANGE,
        type_name='direct',
        durable=True
    )

    await bind_queue_for_channel(
        channel=app.example_channel,
        queue_name=settings.EXAMPLE_MAIN_QUEUE,
        exchange_name=settings.EXAMPLE_EXCHANGE,
        arguments={
            'x-dead-letter-exchange': settings.EXAMPLE_EXCHANGE,
            'x-dead-letter-routing-key': settings.EXAMPLE_MAIN_QUEUE_DLQ
        }
    )
    await bind_queue_for_channel(
        channel=app.example_channel,
        queue_name=settings.EXAMPLE_MAIN_QUEUE_DLQ,
        exchange_name=settings.EXAMPLE_EXCHANGE,
        arguments={
            'x-dead-letter-exchange': settings.EXAMPLE_EXCHANGE,
            'x-dead-letter-routing-key': settings.EXAMPLE_MAIN_QUEUE,
            'x-message-ttl': 5000
        }
    )
    await bind_queue_for_channel(
        channel=app.example_channel,
        queue_name=settings.EXAMPLE_MAIN_QUEUE_ERROR,
        exchange_name=settings.EXAMPLE_EXCHANGE
    )
    asyncio.ensure_future(example_consumer(app), loop=loop)
