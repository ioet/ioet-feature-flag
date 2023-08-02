from abc import ABC, abstractmethod
from typing import Dict


class FeatureRepositoryAdapter(ABC):
    @abstractmethod
    def get_flags(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def set_flag(self, flag_name: str, is_flag_enabled: bool) -> Dict:
        raise NotImplementedError
