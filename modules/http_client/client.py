"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import asyncio
from asyncio import TimeoutError
from json import JSONDecodeError

import aiohttp
import async_timeout
from aiohttp.client_exceptions import ContentTypeError
from sanic.log import logger

from .exceptions import ClientHttpError


class MiddlewareClient:
    def __init__(self):

        self.start_time = None
        self.time_lat = None

        self.trace_config = aiohttp.TraceConfig()
        # трекер начала запроса
        self.trace_config.on_request_start.append(self.on_request_start)
        self.trace_config.on_connection_create_start.append(self.on_request_start)

        # трекер конца запроса
        self.trace_config.on_connection_create_end.append(self.on_request_end)
        self.trace_config.on_request_exception.append(self.on_request_end)

    async def on_request_start(self, _session, _trace_config_ctx, _params):
        self.start_time = asyncio.get_event_loop().time()

    async def on_request_end(self, _session, _trace_config_ctx, _params):
        self.time_lat = asyncio.get_event_loop().time() - self.start_time

    def get_time_lat(self):
        return round(self.time_lat, 3)


class BaseClient(MiddlewareClient):
    response_hooks = []
    request_hooks = []
    timeout = 10

    def __init__(self, service_url=None, timeout=None):
        super().__init__()
        if service_url is not None:
            self.service_url = service_url
        if timeout is not None:
            self.timeout = timeout

    def get_full_url(self, url_name, **kwargs):
        return self.service_url + getattr(self, url_name).format(**kwargs)

    async def get(self, *args, **kwargs):
        return await self.request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.request('POST', *args, **kwargs)

    async def patch(self, *args, **kwargs):
        return await self.request('PATCH', *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self.request('PUT', *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.request('DELETE', *args, **kwargs)

    async def head(self, *args, **kwargs):
        return await self.request('HEAD', *args, **kwargs)

    async def options(self, *args, **kwargs):
        return await self.request('OPTIONS', *args, **kwargs)

    async def request(self, *args, **kwargs):
        request_hooks = kwargs.pop('request_hooks', self.request_hooks)
        response_hooks = kwargs.pop('response_hooks', self.response_hooks)

        for request_hook in request_hooks:
            getattr(self, request_hook)(kwargs)

        http_status = 599
        http_client_name = type(self).__name__
        try:
            async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(verify_ssl=False), trace_configs=[self.trace_config]) as session:
                with async_timeout.timeout(self.timeout):
                    async with session.request(*args, **kwargs) as response:
                        http_status = response.status
                        _response_text = await response.text()
                        try:
                            _response = await response.json()
                        except ContentTypeError:
                            _response = {}
                        except JSONDecodeError:
                            logger.error('request JSONDecodeError text %s', _response_text)
                            _response = {}
                        if http_status >= 400:
                            message = ClientHttpError.MESSAGE.format(
                                http_client_name,
                                kwargs['url'],
                                (args, kwargs),
                                response.status,
                                _response,
                                _response_text
                            )
                            if http_status >= 500:
                                logger.error(f'BaseClient 5xx {http_client_name}: status_code={response.status} '
                                             'url=%s request=%s response=%s response_raw=%',
                                             kwargs['url'], (args, kwargs), _response, _response_text)
                            else:
                                logger.warning(message)
                            raise ClientHttpError(
                                http_client=http_client_name,
                                url=kwargs['url'],
                                request=(args, kwargs),
                                status_code=http_status,
                                response=_response,
                                response_text=_response_text
                            )

                        for response_hook in response_hooks:
                            getattr(self, response_hook)(_response)

                        return _response
        except Exception as ex:
            try:
                logger.exception(f"BaseClient.request HTTP CLIENT ERROR {http_client_name}: "
                                 f"status_code={http_status}; url=%s; args=%s; kwargs=%s",
                                 kwargs.get('url'), args, kwargs)
                raise ex
            except TimeoutError:
                logger.error(f'BaseClient Timeout {http_client_name}: status_code={http_status} '
                             'url=%s request=%s ', kwargs['url'], (args, kwargs))
                raise ClientHttpError(
                    http_client=http_client_name,
                    url=kwargs['url'],
                    request=(args, kwargs),
                    status_code=http_status,
                    response=_response,
                    response_text=_response_text
                )
