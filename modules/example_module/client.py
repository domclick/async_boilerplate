"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from modules.http_client.client import BaseClient

import settings


class TimezoneApiClient(BaseClient):
    service_url = settings.TIMEZONE_API_HOST
    request_hooks = [
        'auth_request',
    ]

    current_time_url = 'timezone/{area}/{city}'

    def auth_request(self, kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'].update({
            # 'Authorization': 'settings.EXAMPLE_TOKEN',
            'Accept': 'application/json'
        })

    async def get_time(self, area, city):
        response = await self.get(self.get_full_url('current_time_url', area=area, city=city))
        return response
