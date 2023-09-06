import abc

import typing


class Strategy(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_attributes(cls, attributes: typing.Dict):
        raise NotImplementedError

    @abc.abstractmethod
    def is_enabled(self) -> bool:
        raise NotImplementedError
