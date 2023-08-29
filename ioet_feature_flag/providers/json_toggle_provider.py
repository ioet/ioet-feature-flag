import json
import typing
import os

from ..exceptions import ToggleNotFoundError, ToggleEnvironmentError
from .provider import Provider
from ..strategies import get_toggle_strategy


class JsonToggleProvider(Provider):
    def __init__(self, toggles_file_path: str) -> None:
        self.path = toggles_file_path
        self._environment = os.getenv("ENVIRONMENT")
        if not self._environment:
            raise ToggleEnvironmentError(
                "Could not retrieve toggles: Toggle environment not specified"
            )

    def get_toggles(self, toggle_names: typing.List[str]) -> typing.Tuple[bool, ...]:
        with open(self.path, "r") as toggles_file:
            toggles = json.load(toggles_file)
            environment_toggles = toggles[self._environment]

            missing_toogles = [
                toggle for toggle in toggle_names if toggle not in environment_toggles
            ]
            if missing_toogles:
                raise ToggleNotFoundError(
                    f"The follwing toggles where not found: {', '.join(missing_toogles)}"
                )

            return tuple(
                get_toggle_strategy(environment_toggles.get(toggle_name)).is_enabled()
                for toggle_name in toggle_names
                if toggle_name in environment_toggles
            )
