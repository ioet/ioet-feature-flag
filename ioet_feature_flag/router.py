import typing

from .providers import Provider
from .exceptions import ToggleNotFoundError
from .strategies import get_toggle_strategy
from .toggle_context import ToggleContext


class Router:
    def __init__(
        self,
        provider: Provider,
    ):
        self._provider = provider

    def get_toggles(
        self,
        toggle_names: typing.Union[typing.List[str], str],
        toggle_context: typing.Optional[ToggleContext] = None,
    ) -> typing.Union[typing.Tuple[bool, ...], bool]:
        if isinstance(toggle_names, str):
            toggle_names = [toggle_names]

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

        toggle_strategies = [
            get_toggle_strategy(toggle_attribute)
            for toggle_attribute in toggle_attributes
        ]

        result = tuple(
            toggle.is_enabled(context=toggle_context) for toggle in toggle_strategies
        )

        if len(result) == 1:
            return result[0]

        return result

    def get_all_toggles(
        self,
        context: typing.Optional[ToggleContext] = None,
    ) -> typing.Dict[str, bool]:
        available_toggles = self._provider.get_toggle_list()

        raw_toggles = {
            toggle_name: self._provider.get_toggle_attributes(toggle_name)
            for toggle_name in available_toggles
        }

        toggle_types = {
            toggle_name: get_toggle_strategy(toggle_attributes)
            for toggle_name, toggle_attributes in raw_toggles.items()
        }

        return {
            toggle_name: toggle.is_enabled(context=context)
            for toggle_name, toggle in toggle_types.items()
        }
