from typing import Callable

from .adapters.base import FeatureRepositoryAdapter


class FeatureRouter:
    def __init__(self, feature_repository: FeatureRepositoryAdapter) -> None:
        self.feature_repository = feature_repository
        self._get_configuration()

    def _get_configuration(self) -> None:
        self.feature_flags = self.feature_repository.get_flags()

    def set_feature_toggle(self, flag_name: str, is_flag_enabled: bool):
        self.feature_flags = self.feature_repository.set_flag(
            flag_name, is_flag_enabled
        )

    def are_features_enabled(self, *flags) -> bool:
        feature_status = True
        for flag in flags:
            feature_status = feature_status and self.feature_flags.get(flag, False)
        return feature_status

    def toggle_point(self, *feature_names):
        def decorator_function(function: Callable):
            def wrapper(*args, **kwargs):
                toggle_point = TogglePoint(
                    toggle_router=self, feature_names=feature_names
                )
                kwargs_with_toggle = {**kwargs, "toggle_point": toggle_point}
                result = function(*args, **kwargs_with_toggle)
                return result

            return wrapper

        return decorator_function


class TogglePoint:
    def __init__(self, toggle_router: FeatureRouter, feature_names):
        self.toggle_router = toggle_router
        self.feature_names = feature_names

    def toggle(self, path_when_enabled: Callable, path_when_disabled: Callable):
        if self.toggle_router.are_features_enabled(*self.feature_names):
            return path_when_enabled()
        return path_when_disabled()
