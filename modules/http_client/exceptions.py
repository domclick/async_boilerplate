"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from core.exceptions import CoreClientError


class ClientHttpError(CoreClientError):
    def __init__(self, http_client=None, url=None, request=None, status_code=None, response=None, response_text=None):
        self.http_client = http_client
        self.url = url
        self.request = request
        self.status_code = status_code

        self.response = {}
        if response:
            self.response = response
        self.response_text = response_text

    MESSAGE = 'HTTP CLIENT ERROR {}: url={}; request={}; status_code={}; response={}; response_raw: {}'

    def __str__(self):
        return self.MESSAGE.format(
            self.http_client,
            self.url,
            self.request,
            self.status_code,
            self.response,
            self.response_text
        )
