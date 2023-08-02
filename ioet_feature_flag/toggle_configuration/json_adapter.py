import os
import json
from typing import List, Tuple


from .base import ToggleConfiguration
from .._exceptions import ToggleNotFoundError


class JSONAdapter(ToggleConfiguration):
    def __init__(self, toggles_file_path: str) -> None:
        self.path = toggles_file_path

    def get_toggles(self, toggle_names: List[str]) -> Tuple[bool, ...]:
        with open(self.path, "r") as toggles_file:
            toggles = json.load(toggles_file)

            missing_toogles = [
                toggle for toggle in toggle_names if toggle not in toggles
            ]
            if missing_toogles:
                raise ToggleNotFoundError(
                    f"The follwing toggles where not found: {', '.join(missing_toogles)}"
                )

            return tuple(
                bool(toggle_value)
                for toggle_name, toggle_value in toggles.items()
                if toggle_name in toggle_names
            )
