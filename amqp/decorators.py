"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from functools import wraps
from sanic.log import logger


def consume_handler(dlq_exchange=None, dlq_routing_key=None, error_dlq_routing_key=None, max_attempts=5):
    """
    :param dlq_exchange:
    :param dlq_routing_key: ключ по которому идут упавшие сообщения
    :param error_dlq_routing_key: ключ когда количество сообщений привысило лимит
    :param max_attempts: количество попыток обработать сообщение
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(channel, body, envelope, properties):
            try:
                result = await func(channel, body, envelope, properties)
            except Exception as e:
                result = False
                logger.exception(f'consume_handler {func.__name__} ex: %s', e)
                headers = properties.headers or {}
                redelivered_count = headers.get('x-redelivered-count', 0)
                if redelivered_count > max_attempts:
                    if error_dlq_routing_key:
                        await channel.publish(
                            payload=body,
                            exchange_name=dlq_exchange,
                            routing_key=error_dlq_routing_key
                        )

                    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
                    return

                if dlq_exchange and dlq_routing_key:
                    await channel.publish(
                        payload=body,
                        exchange_name=dlq_exchange,
                        routing_key=dlq_routing_key,
                        properties={
                            'headers': {
                                'x-redelivered-count': redelivered_count + 1
                            }
                        }
                    )

            await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
            return result

        return wrapper

    return decorator
