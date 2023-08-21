import typing

from .strategy import Strategy


class Static(Strategy):
    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

    def is_enabled(self) -> bool:
        return self._enabled


def build_static_type(metadata: typing.Dict) -> Static:
    return Static(
        enabled=metadata.get('enabled', False),
    )
