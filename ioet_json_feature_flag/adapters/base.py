from abc import ABC, abstractmethod
from typing import Dict


class FeatureRepositoryAdapter(ABC):
    @abstractmethod
    def get_flags(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def set_flag(self, key: str, value: bool) -> Dict:
        raise NotImplementedError
