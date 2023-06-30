import os
import json
from typing import Dict


from .base import FeatureRepositoryAdapter


class JSONAdapter(FeatureRepositoryAdapter):
    def __init__(self, config_path: str) -> None:
        self.config_path = os.path.normpath(config_path)

    def get_flags(self) -> Dict:
        try:
            with open(self.config_path, "r") as configuration_file:
                configuration_flags = json.load(configuration_file)
                return configuration_flags
        except FileNotFoundError:
            return dict()

    def set_flag(self, key: str, value: bool) -> Dict:
        configuration_flags = self.get_flags()
        updated_configuration = {**configuration_flags, key: value}
        self._save_configuration_file(updated_configuration)

        return updated_configuration

    def _save_configuration_file(self, base_configuration: Dict):
        with open(self.config_path, "w") as configuration_file:
            json.dump(base_configuration, configuration_file, indent=2)
