import typing

from .providers import Provider, YamlToggleProvider
from .exceptions import ToggleNotFoundError
from .strategies import get_toggle_strategy

_TOGGLES_LOCATION = './feature_toggles/feature-toggles.yaml'


class Router:
    def __init__(self, provider: typing.Optional[Provider] = None):
        self._provider = provider or YamlToggleProvider(_TOGGLES_LOCATION)

    def get_toggles(self, toggle_names: typing.List[str]) -> typing.Tuple[bool, ...]:
        available_toggles = self._provider.get_toggle_list()

        missing_toogles = [
            toggle for toggle in toggle_names if toggle not in available_toggles
        ]
        if missing_toogles:
            raise ToggleNotFoundError(
                f"The follwing toggles where not found: {', '.join(missing_toogles)}"
            )

        toggle_attributes = [
            self._provider.get_toggle_attributes(toggle_name)
            for toggle_name in toggle_names
        ]

        toggle_types = [
            get_toggle_strategy(toggle_attribute)
            for toggle_attribute in toggle_attributes
        ]

        return tuple(
            toggle.is_enabled()
            for toggle in toggle_types
        )
