import typing

from .strategy import Strategy
from .cutover import build_cutover_type
from .static import build_static_type
from ..exceptions import InvalidToggleType


def get_toggle_strategy(metadata: typing.Dict) -> Strategy:
    toggle_type = metadata.get('type', 'static')
    builders = {
        'static': build_static_type,
        'cutover': build_cutover_type,
    }

    builder = builders.get(toggle_type)
    if not builder:
        allowed_builders = list(builders.keys())
        raise InvalidToggleType(
            f"The provided toggle type {toggle_type} is not valid."
            f" Supported types are {', '.join(allowed_builders)}"
        )

    return builder(metadata)
