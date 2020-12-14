"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from core.exceptions import CoreClientError


class TimeZoneAPiError(CoreClientError):
    def __init__(self, error=None):
        self.error = error
