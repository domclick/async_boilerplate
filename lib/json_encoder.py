"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import datetime
import enum
import json


class DateTimeAndEnumJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.time)):
            return o.replace(tzinfo=datetime.timezone.utc).isoformat()
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, enum.Enum):
            return o.value
        return super().default(o)


class StandartDateTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.time):
            return o.strftime('%H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        return super().default(o)