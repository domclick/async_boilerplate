"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from marshmallow import fields
from sanic_openapi import doc

from lib.schema import BaseSchema


MAP_MARSHMALLOW_IN_OPEN_API = {
    fields.DateTime: doc.DateTime,
    fields.Date: doc.Date,
    fields.Integer: doc.Integer,
    fields.String: doc.String,
    fields.Boolean: doc.Boolean,
    fields.List: doc.List
}


def open_api_schemas(schemas: BaseSchema, is_json: bool = False, many: bool = False):
    """
    Отдает схему для swagger документации получая из marshmallow схему
    """
    swagger_schema = {}
    for field_key in schemas.fields:
        field_obj = schemas.fields[field_key]
        swagger_schema[field_key] = marshmallow_to_swagger(field_key, field_obj)

    if schemas.many is True or many:
        return doc.List(swagger_schema)
    if is_json:
        return doc.JsonBody(swagger_schema)
    return swagger_schema


def open_api_schemas_params(schemas: BaseSchema):
    """
    Отдает схему для swagger документации получая из marshmallow схему
    Для Query-параметров
    """
    params = []
    for field_key in schemas.fields:
        field_obj = schemas.fields[field_key]
        params.append(marshmallow_to_swagger(field_key, field_obj))

    return params


def marshmallow_to_swagger(field_key, field_obj):
    field_type = type(field_obj)
    if isinstance(field_obj, fields.Nested):
        return open_api_schemas(field_obj.schema)
    else:
        doc_type = MAP_MARSHMALLOW_IN_OPEN_API.get(field_type, doc.String)
        required = getattr(field_obj, 'required', False)
        swagger_type = doc_type(name=field_key, required=required)
        if doc_type == doc.List:
            sub_type = type(field_obj.container)
            sub_type = marshmallow_to_swagger(field_obj.container.name, sub_type)
            swagger_type.items = [sub_type]
        return swagger_type
