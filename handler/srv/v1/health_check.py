"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic.log import logger
from sanic.request import Request

from lib.shortcuts.view import http_ok, http_bad_request


async def ping(request: Request):
    try:
        async with request.app.db_engine.acquire() as conn:
            await conn.execute('SELECT 1;')
        return http_ok()
    except Exception:
        logger.exception('ping db fail')
        return http_bad_request(msg='База недоступна')
