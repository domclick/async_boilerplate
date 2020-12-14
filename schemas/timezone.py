"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from marshmallow import fields

from lib.schema import BaseSchema


class GetTimezoneSchema(BaseSchema):
    area = fields.String(required=True)
    city = fields.String(required=True)


class GetTimezoneResultSchema(BaseSchema):
    # описание полей можно посмотреть тут http://worldtimeapi.org/api
    abbreviation = fields.String(required=False)
    client_ip = fields.String(required=False)
    datetime = fields.String(required=False)
    day_of_week = fields.Integer(required=False)
    day_of_year = fields.Integer(required=False)
    dst = fields.Boolean(required=False)
    dst_from = fields.String(required=False)
    dst_offset = fields.Integer(required=False)
    dst_until = fields.String(required=False)
    raw_offset = fields.Integer(required=False)
    timezone = fields.String(required=False)
    unixtime = fields.Integer(required=False)
    utc_datetime = fields.String(required=False)
    utc_offset = fields.String(required=False)
    week_number = fields.Integer(required=False)
