"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import settings
from amqp.decorators import consume_handler
from amqp.consumers.example_consumer import ExampleConsumer


async def example_consumer(app):
    @consume_handler(
        dlq_exchange=settings.EXAMPLE_EXCHANGE,
        dlq_routing_key=settings.EXAMPLE_MAIN_QUEUE_DLQ,
        error_dlq_routing_key=settings.EXAMPLE_MAIN_QUEUE_ERROR,
        max_attempts=3
    )
    async def handle_example_consumer(channel, body, envelope, properties):
        await ExampleConsumer(app).handle(channel, body, envelope, properties)

    await app.example_channel.basic_qos(prefetch_count=10)
    await app.example_channel.basic_consume(
        handle_example_consumer,
        queue_name=settings.EXAMPLE_MAIN_QUEUE,
        no_ack=False
    )
