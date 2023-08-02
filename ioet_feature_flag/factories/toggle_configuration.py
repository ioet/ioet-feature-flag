from ..toggle_configuration import ToggleConfiguration, AWSAppConfigAdapter


def get_toggle_configuration() -> ToggleConfiguration:
    return AWSAppConfigAdapter()
