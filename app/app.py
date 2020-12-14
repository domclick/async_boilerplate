"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from aiopg.sa import create_engine
from sanic import Sanic
from sanic.exceptions import NotFound

from amqp.amqp_config import get_app_config
from amqp.connection import open_amqp_connections, consume_amqp, close_amqp_connections
from core.core_app import AppSanic
from core.logger_config import LOG_SETTINGS

import routes
import settings as s
from schedule import initialize_scheduler
from lib.shortcuts.view import http_not_found


async def handle_404(_request, _exception):
    return http_not_found()


async def setup_connect(app: AppSanic, _loop):
    app.db_engine = await create_engine(
        user=s.DB_USER,
        password=s.DB_PASSWORD,
        host=s.DB_HOST,
        port=s.DB_PORT,
        database=s.DB_NAME,
        maxsize=s.DB_MAX_CONNECTIONS,
        application_name=s.APP_NAME,
        pool_recycle=s.DC_POOL_RECYCLE,
    )


async def close_connect(app: AppSanic, _loop):
    app.db_engine.close()
    await app.db_engine.wait_closed()


async def schedule_initializer(app, loop):
    scheduler_instance = initialize_scheduler(app, loop)
    scheduler_instance.start()


async def setup_amqp_connection(app, loop):
    await open_amqp_connections(app, config=get_app_config())


async def start_consume_amqp(app, loop):
    await consume_amqp(app, loop)


async def close_amqp_connection(app, loop):
    await close_amqp_connections(app, config=get_app_config())


def set_router(app: Sanic):
    if s.DEBUG:
        # Fix для sanic_openapi
        from core.swagger import swagger_init
        app.blueprint(swagger_init())
    app.blueprint(routes.api)


def get_port(api=False, consume=False, schedule=False):
    if consume:
        return s.AMQ_PORT
    if schedule:
        return s.SCHEDULE_PORT
    return s.API_PORT


def init_app(api=False, consume=False, schedule=False) -> AppSanic:
    app = AppSanic(__name__, log_config=LOG_SETTINGS, strict_slashes=True)
    app.exception(NotFound)(handle_404)

    app.listener('before_server_start')(setup_connect)
    app.listener('before_server_stop')(close_connect)

    if api:
        set_router(app)

    if consume:
        app.listener('before_server_start')(setup_amqp_connection)
        app.listener('after_server_start')(start_consume_amqp)

        app.listener('before_server_stop')(close_amqp_connection)

    if schedule:
        app.listener('before_server_start')(schedule_initializer)

    app.blueprint(routes.srv)
    return app
