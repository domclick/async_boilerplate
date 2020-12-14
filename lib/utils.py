"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import enum
import json
import re
import time
from collections import OrderedDict
from functools import wraps
from typing import Iterable

from marshmallow import ValidationError
from sanic.log import logger

from lib.json_encoder import DateTimeAndEnumJSONEncoder, StandartDateTimeJSONEncoder

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def load_data(engine, table, data, erase_all=True):
    if erase_all:
        engine.execute(f'ALTER TABLE \"{str(table)}\" DISABLE TRIGGER ALL;')
        engine.execute(table.delete())
        engine.execute(f'ALTER TABLE \"{str(table)}\" ENABLE TRIGGER ALL;')
    if type(data) == dict:
        row = convert_bool(data)
        engine.execute(table.insert().values(**row))
    elif len(data) == 1:
        row = convert_bool(data[0])
        engine.execute(table.insert().values(**row))
    else:
        for item in data:
            row = convert_bool(item)
            engine.execute(table.insert().values(**row))

    # Переводит sequence в актуальное состояние, на всякий случай, так как при загрузуке фикстур с id,
    # в pg не вызывается автоинкремент sequence
    if 'id' in table.columns:
        sequence = '{}_id_seq'.format(table.name)
        engine.execute("ALTER SEQUENCE {} RESTART".format(sequence))
        engine.execute("SELECT setval('{}', (SELECT max(id) FROM \"{}\"))".format(sequence, table.name))


def convert_bool(data: dict) -> dict:
    for k, v in data.items():
        if isinstance(v, str) and len(v) == 1:
            try:
                data[k] = int(v)
            except ValueError:
                continue
    return data


def async_step(func):
    @wraps(func)
    def synced_func(*args, **kwargs):
        loop = kwargs.get("loop")
        if not loop:
            raise Exception("Need loop fixture to make function sync")
        return loop.run_until_complete(func(*args, **kwargs))

    return synced_func


class NoneType:
    pass


class BaseEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return [k.value for k in cls]

    @classmethod
    def get_value_by_key(cls, key):
        return getattr(cls, key).value


class BaseIntEnum(BaseEnum, enum.IntEnum):
    pass


def list_validate(lst: tuple):
    from marshmallow import ValidationError

    def validate(n):
        if n and n not in lst:
            raise ValidationError('Invalid option.')

    return validate


def custom_dumps(obj, isoformat=True):
    if isoformat:
        return json.dumps(obj, cls=DateTimeAndEnumJSONEncoder)
    return json.dumps(obj, cls=StandartDateTimeJSONEncoder)


def ignore_exception(func):
    """
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.exception(f'ignore_exception {func.__name__} ex {ex.__class__.__name__} error: %s', ex)

    return wrapper


def make_marshmallow_errors_list(errors):
    errors_list = []
    for key, value in sorted(errors.items(), key=lambda x: str(x[0])):
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
                            'code': '.'.join([key, str(i), fieldname]),
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
    return errors_list


def check_ids(data, fields_name, msg_text='Только числа разделенные запятой'):
    if data.get(fields_name):
        if type(data.get(fields_name)) == str:
            ids = []
            for sid in data[fields_name].split(','):
                if not sid.isdigit():
                    raise ValidationError({fields_name: [msg_text]})
                ids.append(int(sid))
            data[fields_name] = ids
        if type(data.get(fields_name)) == int:
            data[fields_name] = [data[fields_name]]


def dict_filter(d: dict, keys: Iterable) -> dict:
    return {k: d[k] for k in keys}


def is_time_format(value):
    try:
        time.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False


def camel_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def underscoreize(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = camel_to_underscore(key)
            new_dict[new_key] = underscoreize(value)
        return new_dict
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = underscoreize(data[i])
        return data
    return data


def underscore_to_camel(match):
    return match.group()[0] + match.group()[2].upper()


def camelize(data, exclude_keys=None):
    if exclude_keys is None:
        exclude_keys = []

    if isinstance(data, dict):
        new_dict = OrderedDict()
        for key, value in data.items():
            new_key = re.sub(r"[a-z]_[a-z]", underscore_to_camel, key)
            if key not in exclude_keys:
                new_dict[new_key] = camelize(value)
            else:
                new_dict[new_key] = value
        return dict(new_dict)
    if isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = camelize(data[i])
        return data
    return data


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def str_to_bool(text: str) -> bool:
    return True if text in ['true', 'True', True, '1'] else False


def filter_fields(fields, data_dict):
    return {k: v for k, v in data_dict.items() if k in fields}
