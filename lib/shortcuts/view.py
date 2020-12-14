"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic import response
from sanic.log import logger

from lib.utils import custom_dumps


def _error_http_response(msg: str, code: int, headers=None):
    resp = response.json({
        'success': False,
        'errors': [{'code': code, 'message': msg}] if isinstance(msg, str) else msg
    }, status=code, dumps=custom_dumps)
    if headers:
        resp.headers.update(headers)

    return resp


def _http_response(data: object, code: int, headers=None):
    resp = response.json({
        'success': True,
        'result': data
    }, status=code, dumps=custom_dumps)
    if headers:
        resp.headers.update(headers)

    return resp


def http_ok(msg='OK', headers=None):
    code = 200

    return _http_response(msg, code, headers)


def http_created(msg='Created', headers=None):
    code = 201
    return _http_response(msg, code, headers)


def http_empty(headers=None):
    code = 204
    return _http_response('', code, headers=headers)


def http_bad_request(msg='Bad request', headers=None):
    code = 400
    return _error_http_response(msg, code, headers=headers)


def http_unauthorized(msg='Unauthorized', headers=None):
    code = 401
    return _error_http_response(msg, code, headers=headers)


def http_forbidden(msg='Forbidden', headers=None):
    code = 403
    return _error_http_response(msg, code, headers=headers)


def http_not_found(msg='Not found', headers=None):
    code = 404
    return _error_http_response(msg, code, headers=headers)


def http_request_timeout(msg='Request timeout', headers=None):
    code = 408
    return _error_http_response(msg, code, headers=headers)


def http_conflict(msg='Conflict', headers=None):
    code = 409
    return _error_http_response(msg, code, headers=headers)


def marshmallow_errors(errors):
    errors_list = []
    try:
        for key, value in errors.items():
            if isinstance(value, list):
                errors_list.append({
                    'code': key,
                    'message': ','.join(value)
                })
            elif isinstance(value, dict):
                # Значит ошибка имеет вид:
                # {'services': {
                #     0: {'service_type_id': ['Missing data for required field.']},
                #     1: {'service_type_id': ['Missing data for required field.']}}}
                for i, error_data_object in value.items():
                    if isinstance(error_data_object, list):
                        for err_text in error_data_object:
                            errors_list.append({
                                'code': '.'.join([str(key), str(i)]),
                                'message': err_text
                            })
                    elif isinstance(error_data_object, dict):
                        for fieldname, error_data in error_data_object.items():
                            errors_list.append({
                                'code': '.'.join([str(key), str(i), fieldname]),
                                'message': ','.join(error_data)
                            })
                    else:
                        errors_list.append({
                            'code': key,
                            'message': str(value)
                        })
            else:
                errors_list.append({
                    'code': key,
                    'message': str(value)
                })
    except Exception as exc:
        logger.exception(f'marshmallow_errors get exception - {exc}')
    return response.json({
        'success': False,
        'errors': errors_list

    }, status=400)
