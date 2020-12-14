"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from aiopg.sa import Engine
from sanic import Sanic


class AppSanic(Sanic):
    db_engine: Engine
