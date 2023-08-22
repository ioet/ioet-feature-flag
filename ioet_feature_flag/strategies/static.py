import typing

from .strategy import Strategy


class Static(Strategy):
    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    @classmethod
    def from_metadata(cls, metadata: typing.Dict) -> "Static":
        return cls(
            enabled=metadata.get('enabled', False),
        )

    def is_enabled(self) -> bool:
        return self._enabled
