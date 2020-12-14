"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import os

from envparse import Env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = Env()
env_file_path = os.path.join(BASE_DIR, '.env')
env.read_envfile(env_file_path)

APP_NAME = 'app_name'
HOST = env.str('HOST', default='0.0.0.0')

API_PORT = env.int('API_PORT', default=8090)
AMQ_PORT = env.int('AMQ_PORT', default=8091)
SCHEDULE_PORT = env.int('SCHEDULE_PORT', default=8092)

WORKERS = env.int('WORKERS', default=1)

ENV = env.str('ENV', default='local')
DEBUG = env.bool('DEBUG', default=False)
AUTO_RELOAD = env.bool('AUTO_RELOAD', default=False)

DB_HOST = env.str('DB_HOST', default='localhost')
DB_PORT = env.int('DB_PORT', default=5455)
DB_NAME = env.str('DB_NAME', default='example')
DB_USER = env.str('DB_USER', default='example')
DB_PASSWORD = env.str('DB_PASSWORD', default='example')
DB_MAX_CONNECTIONS = env.int('DB_MAX_CONNECTIONS', default=10)
DC_POOL_RECYCLE = env.int('DC_POOL_RECYCLE', default=60)

EXAMPLE_AMQP_HOST = env.str('EXAMPLE_AMQP_HOST', default='localhost')
EXAMPLE_AMQP_USER = env.int('EXAMPLE_AMQP_USER', default='guest')
EXAMPLE_AMQP_PASS = env.str('EXAMPLE_AMQP_PASS', default='guest')
EXAMPLE_AMQP_VHOST = env.str('EXAMPLE_AMQP_VHOST', default='/')
EXAMPLE_AMQP_PORT = env.str('EXAMPLE_AMQP_PORT', default=5672)

EXAMPLE_EXCHANGE = env.str('EXAMPLE_EXCHANGE', default='example.exchange')
EXAMPLE_MAIN_QUEUE = env.str('EXAMPLE_MAIN_QUEUE', default='example.main')
EXAMPLE_MAIN_QUEUE_DLQ = env.str('EXAMPLE_MAIN_QUEUE_DLQ', default='example.main.dlq')
EXAMPLE_MAIN_QUEUE_ERROR = env.str('EXAMPLE_MAIN_QUEUE_ERROR', default='example.main.error')

# reconnect to rabbitmq
RECONNECT_RESTART_COUNT = env.int('RECONNECT_RESTART_COUNT', default=10)
RECONNECT_SLEEP_TIME = env.int('RECONNECT_SLEEP_TIME', default=5)

TIMEZONE_API_HOST = env.str('TIMEZONE_API_HOST', default='http://worldtimeapi.org/api/')