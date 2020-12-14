"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic import response
from sanic_openapi import swagger_blueprint


def spec(_):
    ret = swagger_blueprint._spec.__dict__
    ret["swagger"] = "2.0"
    return response.json(ret)


def swagger_init():
    blueprint = swagger_blueprint

    uri = '/swagger.json'
    index = [i for i, v in enumerate(blueprint.routes) if v.uri == uri][0]
    del blueprint.routes[index]
    blueprint.route(uri)(spec)
    return blueprint
