import os
from appconfig_helper import AppConfigHelper
from ioet_featureflag.providers.base_provider import Provider

class AWSAppConfigProvider(Provider):
    def __init__(
        self,
        appconfig_app: str,
        appconfig_env: str,
        appconfig_profile: str,
        appconfig_update_interval: int = 45,
    ):
        self.appconfig = AppConfigHelper(
            appconfig_app,
            appconfig_env,
            appconfig_profile,
            appconfig_update_interval,
        )

    def set_flag(self, feature_name: str):
        pass

    def get_flag(self, feature_name: str, default_value: bool = False) -> bool:
        self.appconfig.update_config()
        return self.appconfig.config.get(feature_name, default_value)