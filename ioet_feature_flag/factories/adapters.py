from ..toggle_configuration.base import FeatureRepositoryAdapter
from ..toggle_configuration.json_adapter import JSONAdapter


def get_toggle_configuration() -> FeatureRepositoryAdapter:
    return JSONAdapter(config_path="feaure_toggles.json")
