from functools import wraps

import typing

from . import exceptions, types
from .providers import Provider, YamlToggleProvider
from .router import Router


_TOGGLES_LOCATION = './feature_toggles/feature-toggles.yaml'


class Toggles:
    def __init__(self, provider: typing.Optional[Provider] = None) -> None:
        self._router = Router(provider)

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

            return decision_function(self._router.get_toggles, when_on, when_off)

        return _wraps
