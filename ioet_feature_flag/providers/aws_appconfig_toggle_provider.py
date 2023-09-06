import os
import typing
from ..helpers import AppConfigHelper
from ..exceptions import ToggleNotFoundError
from .provider import Provider


class AWSAppConfigToggleProvider(Provider):
    def __init__(self) -> None:
        self._appconfig = AppConfigHelper(
            os.environ["AWS_APPCONFIG_APP"],
            os.environ["AWS_APPCONFIG_ENV"],
            os.environ["AWS_APPCONFIG_PROFILE"],
            os.environ.get("AWS_APPCONFIG_MAX_CONFIG_AGE", 45),
        )

    def get_toggle_list(self) -> typing.List[str]:
        toggles: typing.Dict = self._appconfig.config
        return list(toggles.keys())

    def get_toggle_attributes(self, toggle_name: str) -> typing.Dict:
        toggles: typing.Dict = self._appconfig.config
        toggle_attributes = toggles.get(toggle_name)
        if not toggle_attributes:
            raise ToggleNotFoundError(
                f"The toggle {toggle_name} was not found in the"
                f" {os.environ.get('AWS_APPCONFIG_ENV')} environment."
            )
        return toggle_attributes
