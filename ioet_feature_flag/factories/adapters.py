from ..adapters.base import FeatureRepositoryAdapter
from ..adapters.json_adapter import JSONAdapter


def get_toggle_configuration() -> FeatureRepositoryAdapter:
    return JSONAdapter(config_path="feaure_toggles.json")
