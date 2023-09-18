import typing

from .strategy import Strategy
from ..toggle_context import ToggleContext


class Static(Strategy):
    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "Static":
        return cls(
            enabled=attributes.get("enabled", False),
        )

    def is_enabled(self, context: typing.Optional[ToggleContext] = None) -> bool:
        return self._enabled
