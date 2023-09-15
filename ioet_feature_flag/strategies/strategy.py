import abc

import typing

from ..toggle_context import ToggleContext


class Strategy(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_attributes(cls, attributes: typing.Dict):
        raise NotImplementedError

    @abc.abstractmethod
    def is_enabled(self, context: typing.Optional[ToggleContext] = None) -> bool:
        raise NotImplementedError
