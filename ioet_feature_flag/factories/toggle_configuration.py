from ..toggle_configuration.base import ToggleConfiguration
from ..toggle_configuration.json_adapter import JSONAdapter


def get_toggle_configuration() -> ToggleConfiguration:
    return JSONAdapter(toggles_file_path="feature_toggles.json")
