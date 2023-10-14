import typing

from .strategy import Strategy
from ..exceptions import MissingToggleAttributes, InvalidToggleAttribute
from ..toggle_context import ToggleContext


class PilotUsers(Strategy):
    def __init__(self, enabled: bool, allowed_users: typing.List[str]) -> None:
        self._enabled = enabled
        self._allowed_users = allowed_users

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "PilotUsers":
        allowed_users: typing.List[str] = attributes.get("allowed_users")
        if not allowed_users:
            raise MissingToggleAttributes("You must provide a list of allowed users")

        if not isinstance(allowed_users, list):
            raise InvalidToggleAttribute("The provided users must be in a list")

        return cls(
            enabled=attributes.get("enabled", False),
            allowed_users=[user.strip() for user in allowed_users],
        )

    def is_enabled(self, context: ToggleContext) -> bool:
        return self._enabled and context.username in self._allowed_users
