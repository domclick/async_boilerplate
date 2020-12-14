"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from marshmallow import fields
from lib.schema import BaseSchema


class CreateStudentSchema(BaseSchema):
    name = fields.String(required=True)


class UpdateStudentSchema(BaseSchema):
    name = fields.String(required=True)


class StudentResultSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    active = fields.Boolean(required=True)
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S+00:00', required=True)
    updated_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S+00:00', required=True)
