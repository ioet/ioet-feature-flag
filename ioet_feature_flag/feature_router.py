from typing import Tuple, List
from abc import ABC, abstractmethod

from .toggle_configuration.base import ToggleConfiguration
from .factories.toggle_configuration import get_toggle_configuration


class FeatureRouter(ABC):
    def __init__(
        self, toggle_configuration: ToggleConfiguration = get_toggle_configuration()
    ) -> None:
        self._toggle_configuration = toggle_configuration

    def _get_toggles(self, toggle_names: List[str]) -> Tuple[bool, ...]:
        return self._toggle_configuration.get_toggles(toggle_names=toggle_names)

    @abstractmethod
    def __call__(self) -> bool:
        raise NotImplementedError
