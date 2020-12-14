"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import json

from sanic.log import logger

from models.student import Student


class ExampleConsumer:
    def __init__(self, app):
        self.app = app

    async def handle(self, channel, body, envelope, properties):
        logger.info('incoming msg {}'.format(body))
        data = json.loads(body.decode())
        async with self.app.db_engine.acquire() as conn:
            await Student.create(conn=conn, values=data)
