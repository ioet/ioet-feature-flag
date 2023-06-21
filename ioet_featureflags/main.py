import typing

from provider import Provider

class FeatureFlags:
    def __init__(
        self,
        provider: Provider,
    ):
        self.provider = provider

    def is_enabled(self, feature_name: str, default_value: bool = False) -> bool:
        return self.provider.get_flag(feature_name, default_value)

    def on(self, feature_name: str, default_value: bool = False):
        def decorator(function):
            return self.handler(
                is_enabled=self.is_enabled(feature_name, default_value),
                when_on=function,
                when_off=lambda: None,
            )
        return decorator

    def off(self, feature_name: str, default_value: bool = False):
        def decorator(function):
            return self.handler(
                is_enabled=self.is_enabled(feature_name, default_value),
                when_on=lambda: None,
                when_off=function,
            )
        return decorator

    def handler(cls, is_enabled: bool, when_on: typing.Callable, when_off: typing.Callable):
        def wrapper(*args, **kwargs):
            return when_on(*args, **kwargs) if is_enabled else when_off(*args, **kwargs)
        return wrapper

    def enable_feature(self, feature_name: str) -> bool:
        self.provider.set_flag(feature_name, True)

    def disable_feature(self, feature_name: str) -> bool:
        self.provider.set_flag(feature_name, False)
