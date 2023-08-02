import os
from appconfig_helper import AppConfigHelper
from typing import List, Tuple, Dict


from .base import ToggleConfiguration
from .._exceptions import ToggleNotFoundError


class AWSAppConfigAdapter(ToggleConfiguration):
    def __init__(self) -> None:
        self._appconfig = AppConfigHelper(
            os.environ["AWS_APPCONFIG_APP"],
            os.environ["AWS_APPCONFIG_ENV"],
            os.environ["AWS_APPCONFIG_PROFILE"],
            os.environ.get("AWS_APPCONFIG_MAX_CONFIG_AGE", 45),
        )

    def get_toggles(self, toggle_names: List[str]) -> Tuple[bool, ...]:
        self._appconfig.update_config()
        toggles: Dict = self._appconfig.config

        missing_toogles = [toggle for toggle in toggle_names if toggle not in toggles]
        if missing_toogles:
            raise ToggleNotFoundError(
                f"The follwing toggles where not found: {', '.join(missing_toogles)}"
            )

        return tuple(
            bool(toggle_value.get("enabled"))
            for toggle_name, toggle_value in toggles.items()
            if toggle_name in toggle_names
        )
