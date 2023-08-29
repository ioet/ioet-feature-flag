import os
import typing
from ..helpers import AppConfigHelper
from ..exceptions import ToggleNotFoundError
from .provider import Provider
from ..strategies import get_toggle_strategy


class AWSAppConfigToggleProvider(Provider):
    def __init__(self) -> None:
        self._appconfig = AppConfigHelper(
            os.environ["AWS_APPCONFIG_APP"],
            os.environ["AWS_APPCONFIG_ENV"],
            os.environ["AWS_APPCONFIG_PROFILE"],
            os.environ.get("AWS_APPCONFIG_MAX_CONFIG_AGE", 45),
        )

    def get_toggles(self, toggle_names: typing.List[str]) -> typing.Tuple[bool, ...]:
        self._appconfig.update_config()
        toggles: typing.Dict = self._appconfig.config

        missing_toogles = [
            toggle for toggle in toggle_names if toggle not in toggles
        ]
        if missing_toogles:
            raise ToggleNotFoundError(
                f"The follwing toggles where not found: {', '.join(missing_toogles)}"
            )

        return tuple(
            get_toggle_strategy(toggles.get(toggle_name)).is_enabled()
            for toggle_name in toggle_names
            if toggles.get(toggle_name)
        )
