import typing

from .strategy import Strategy
from ..exceptions import MissingToggleAttributes
from ..toggle_context import ToggleContext


class PilotUsers(Strategy):
    def __init__(self, enabled: bool, allowed_users: typing.List[str]) -> None:
        self._enabled = enabled
        self._allowed_users = allowed_users

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "PilotUsers":
        allowed_users: str = attributes.get('allowed_users')
        if not allowed_users:
            raise MissingToggleAttributes("You must provide a list of allowed users")

        return cls(
            enabled=attributes.get('enabled', False),
            allowed_users=allowed_users.split(','),
        )

    def is_enabled(self, context: ToggleContext) -> bool:
        return self._enabled and context.username in self._allowed_users
