"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""


class CoreAppError(Exception):
    """
    Базовая ошибка приложения, желательно от неё наследовать все ошибки
    """
    pass


class CoreViewError(CoreAppError):
    """
    Базовая ошибка для пользователя
    """
    def __init__(self, mes: str, log: str = None, *args, **kwargs):
        self.err = self.__class__.__name__

        self.mes = mes

        self.log = log
        if not log:
            self.log = mes

        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return f"ex={self.err} log={self.log}"

    def __repr__(self):
        return str(self)


class CoreClientError(CoreAppError):
    pass


class ModulesError(CoreClientError):
    pass
