import os
from appconfig_helper import AppConfigHelper
from typing import Dict


from .base import FeatureRepositoryAdapter


class AWSAppConfigAdapter(FeatureRepositoryAdapter):
    def __init__(self) -> None:
        self._appconfig = AppConfigHelper(
            os.environ["AWS_APPCONFIG_APP"],
            os.environ["AWS_APPCONFIG_ENV"],
            os.environ["AWS_APPCONFIG_PROFILE"],
            os.environ.get("AWS_APPCONFIG_MAX_CONFIG_AGE", 45),
        )

    def get_flags(self) -> Dict:
        self._appconfig.update_config()
        return self._appconfig.config

    def set_flag(self, flag_name: str, is_flag_enabled: bool) -> Dict:
        if not self._appconfig.config.get(flag_name):
            self._appconfig.config[flag_name] = {}
        self._appconfig.config[flag_name]['enabled'] = is_flag_enabled
        return self._appconfig.config
