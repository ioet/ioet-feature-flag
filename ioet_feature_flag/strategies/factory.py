import typing

from .strategy import Strategy
from .cutover import Cutover
from .static import Static
from ..exceptions import InvalidToggleType


def get_toggle_strategy(metadata: typing.Dict) -> Strategy:
    toggle_type = metadata.get('type', 'static')
    strategies = {
        'static': Static,
        'cutover': Cutover,
    }

    strategy: Strategy = strategies.get(toggle_type)
    if not strategy:
        allowed_builders = list(strategies.keys())
        raise InvalidToggleType(
            f"The provided toggle type {toggle_type} is not valid."
            f" Supported types are {', '.join(allowed_builders)}"
        )

    return strategy.from_metadata(metadata)
