import typing

from .strategy import Strategy
from .cutover import Cutover
from .static import Static
from .pilot_users import PilotUsers
from ..exceptions import InvalidToggleType


def get_toggle_strategy(attributes: typing.Dict) -> Strategy:
    toggle_type = attributes.get('type', 'static')
    strategies = {
        'static': Static,
        'cutover': Cutover,
        'pilot_users': PilotUsers,
    }

    strategy: Strategy = strategies.get(toggle_type)
    if not strategy:
        allowed_builders = list(strategies.keys())
        raise InvalidToggleType(
            f"The provided toggle type {toggle_type} is not valid."
            f" Supported types are {', '.join(allowed_builders)}"
        )

    return strategy.from_attributes(attributes)
