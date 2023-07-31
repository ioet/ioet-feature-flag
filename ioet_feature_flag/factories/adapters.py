from ..adapters.base import FeatureRepositoryAdapter
from ..adapters.aws_appconfig_adapter import AWSAppConfigAdapter


def get_toggle_configuration() -> FeatureRepositoryAdapter:
    return AWSAppConfigAdapter()
