import typing
from provider import Provider

class AWSAppConfigProvider(Provider):
    def __init__(
        self,
        config: typing.Dict = {}
    ):
        self.config = config

    def set_flag(self, feature_name: str, value: bool):
        self.config[feature_name] = value

    def get_flag(self, feature_name: str, default_value: bool = False) -> bool:
        return self.config.get(feature_name, default_value)
