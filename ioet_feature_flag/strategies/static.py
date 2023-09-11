import typing

from .strategy import Strategy


class Static(Strategy):
    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "Static":
        return cls(
            enabled=attributes.get('enabled', False),
        )

    def is_enabled(self) -> bool:
        return self._enabled
