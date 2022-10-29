from typing import Any


class GeneralException(Exception):
    def __init__(self, msg: dict[Any, list[Any]]) -> None:
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        _out = "GeneralException:\n"
        for key, values in self.msg.items():
            _out += f"\t> {key}:\n"
            for value in values:
                _out += f"\t\t> {value}\n"
        return _out


class InvalidInputException(GeneralException):
    pass


class TokenException(GeneralException):
    pass


class DataException(GeneralException):
    pass


class PayloadException(Exception):
    def __init__(self, *msgs):
        self.msgs = msgs
        super().__init__(msgs)

    def __str__(self) -> str:
        _count = 1
        _output = "\n"
        for msg in self.msgs:
            _output += f"{_count}. {msg}\n"
            _count += 1

        return _output


class ExceptionMap(dict):
    _Default_Exception = GeneralException

    def __init__(self):
        self.__setitem__("invalid access-token", TokenException)

    def __getitem__(self, __key):
        try:
            return super().__getitem__(__key)
        except KeyError:
            return self._Default_Exception
