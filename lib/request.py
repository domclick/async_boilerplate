"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from functools import wraps
from typing import Type

from marshmallow import Schema, ValidationError
from sanic.exceptions import InvalidUsage
from sanic.request import Request
from sanic import response

from lib.shortcuts.view import marshmallow_errors, http_bad_request


def _error_no_data(target):
    payload = {
        'success': False,
        'errors': [
            {'code': 400, 'message': f'No request {target} provided'}
        ]
    }
    return response.json(payload)


class ValidateRequest:
    """
    Validate request with marshmallow schema
    """

    def __init__(self, schema: Type[Schema], target: str, many: bool = False,
                 partial: bool = False, empty: bool = False):

        assert target in ['args', 'json'], 'Wrong target. Expected `args`, `json`'

        self._target = target
        self._schema = schema
        self._many = many
        self._partial = partial
        self._empty = empty

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[0] if isinstance(args[0], Request) else args[1]

            try:
                target_data = getattr(request, self._target)
            except InvalidUsage:
                return http_bad_request('data is not json')

            if not target_data and not self._empty:
                return _error_no_data(self._target)
            elif self._empty and target_data is None:
                target_data = {}

            schema = self._schema(partial=self._partial, many=self._many)

            try:
                validated_data = schema.load(target_data)
            except ValidationError as errors:
                return marshmallow_errors(errors.messages)

            request[f'validated_{self._target}'] = validated_data
            return await func(*args, **kwargs)

        return wrapper


def validate_json(schema: Type[Schema], many: bool = False, partial: bool = False, empty: bool = False):
    """
    Validate request json with marshmallow schema
    """
    return ValidateRequest(schema=schema, target='json', many=many, partial=partial, empty=empty)


def validate_args(schema: Type[Schema], partial: bool = False, empty: bool = False):
    """
    Validate request args with marshmallow schema
    """
    return ValidateRequest(schema=schema, target='args', many=False, partial=partial, empty=empty)
