from typing import Type, TypeVar, Callable
from functools import wraps

from .feature_router import FeatureRouter
from ._exceptions import InvalidDecisionParameters


TOGGLED_VALUE = TypeVar("TOGGLED_VALUE")


class TogglePoint:
    def __init__(self, toggle_router: Type[FeatureRouter]):
        self.toggle_router = toggle_router()

    def __call__(
        self,
        function: Callable[
            ["TogglePoint", TOGGLED_VALUE, TOGGLED_VALUE], TOGGLED_VALUE
        ],
    ):
        @wraps(function)
        def _wrapper(when_on: TOGGLED_VALUE, when_off: TOGGLED_VALUE) -> TOGGLED_VALUE:
            if str(type(when_off)) != str(type(when_on)):
                raise InvalidDecisionParameters(
                    (
                        "when_on and when_off parameters must be of the same type. "
                        f"when_on parameter is {str(type(when_on))} and when_off parameter is {str(type(when_off))}"
                    )
                )
            return function(toggle_point=self, when_on=when_on, when_off=when_off)

        return _wrapper

    def toggle(self, when_on: TOGGLED_VALUE, when_off: TOGGLED_VALUE) -> TOGGLED_VALUE:
        if self.toggle_router():
            return when_on
        return when_off
