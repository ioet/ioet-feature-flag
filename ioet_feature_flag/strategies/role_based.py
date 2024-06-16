import typing

from .strategy import Strategy
from ..exceptions import (
    MissingToggleAttributes,
    InvalidToggleAttribute,
    MissingToggleContext,
)
from ..toggle_context import ToggleContext


class RoleBased(Strategy):
    def __init__(self, enabled: bool, allowed_roles: typing.List[str]) -> None:
        self._enabled = enabled
        self._allowed_roles = allowed_roles

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "RoleBased":
        allowed_roles: typing.List[str] = attributes.get("roles")
        if not allowed_roles:
            raise MissingToggleAttributes("You must provide a list of allowed roles")

        if not isinstance(allowed_roles, list):
            raise InvalidToggleAttribute("The provided roles must be in a list")

        return cls(
            enabled=attributes.get("enabled", False),
            allowed_roles=[role.strip() for role in allowed_roles],
        )

    def is_enabled(self, context: typing.Optional[ToggleContext] = None) -> bool:
        if not context:
            raise MissingToggleContext(
                "Toggle context is required to compute toggle's state"
            )

        return self._enabled and context.role in self._allowed_roles
