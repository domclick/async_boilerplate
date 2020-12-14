"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from urllib.request import Request

from sanic_openapi import doc

from lib.request import validate_args
from lib.swagger import open_api_schemas_params, open_api_schemas
from schemas.timezone import GetTimezoneSchema, GetTimezoneResultSchema
from modules.example_module.client import TimezoneApiClient
from lib.shortcuts.view import http_bad_request, http_ok


@doc.summary('Получить информацию по таймзоне')
@doc.consumes(*open_api_schemas_params(GetTimezoneSchema()), location='query', required=True)
@doc.produces(open_api_schemas(GetTimezoneResultSchema()))
@validate_args(schema=GetTimezoneSchema)
async def get_timezone(request: Request):
    area, city = request['validated_args']['area'], request['validated_args']['city']
    result = await TimezoneApiClient(timeout=30).get_time(area=area, city=city)
    if not result:
        return http_bad_request(f'timezone with area={area} and city={city} not found')
    return http_ok(GetTimezoneResultSchema().dump(result))
