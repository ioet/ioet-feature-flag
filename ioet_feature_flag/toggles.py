import typing

from functools import wraps

from . import exceptions, types
from .providers import Provider, JsonToggleProvider


class Toggles:
    def __init__(
        self,
        provider: typing.Optional[Provider] = None,
    ) -> None:
        if provider:
            self.provider = provider
            return
        self.provider = JsonToggleProvider('./toggles/toggles.json')

    def toggle_decision(self, decision_function: types.TOOGLE_DECISION):
        @wraps(decision_function)
        def _wraps(
            when_on: types.TOGGLED_VALUE,
            when_off: types.TOGGLED_VALUE,
        ):
            if str(type(when_on)) != str(type(when_off)):
                raise exceptions.InvalidDecisionFunction(
                    (
                        "when_on and when_off parameters must be of the same type. "
                        f"when_on parameter is {str(type(when_on))} and "
                        f"when_off parameter is {type(when_off)}"
                    )
                )

            if isinstance(when_on, bool) or isinstance(when_off, bool):
                raise exceptions.InvalidDecisionFunction(
                    (
                        "when_on and when_off parameters can't be boolean. "
                        "We have added this restriction to avoid a lot of is statements in your app"
                    )
                )

            return decision_function(self.provider.get_toggles, when_on, when_off)

        return _wraps
