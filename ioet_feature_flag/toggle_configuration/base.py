from abc import ABC, abstractmethod
from typing import Tuple, List


class ToggleConfiguration(ABC):
    @abstractmethod
    def get_toggles(self, toggle_names: List[str]) -> Tuple[bool, ...]:
        raise NotImplementedError
