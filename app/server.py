"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic.log import logger

from settings import DEBUG, HOST, WORKERS
from .app import init_app, get_port


def run(api=False, consume=False, schedule=False):
    app = init_app(api=api, consume=consume, schedule=schedule)
    port = get_port(api=api, consume=consume, schedule=schedule)
    try:
        app.go_fast(
            host=HOST,
            port=port,
            workers=WORKERS,
            debug=DEBUG,
            auto_reload=False
        )
    except Exception as ex:
        logger.exception("stop_app ex=%s", ex)
        raise
