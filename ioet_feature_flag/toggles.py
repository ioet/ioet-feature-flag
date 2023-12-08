from pathlib import Path
from functools import wraps

import typing

from . import exceptions, types
from .providers import Provider
from .router import Router
from .toggle_context import ToggleContext
from .helpers import validators


class Toggles:
    def __init__(
        self, project_root: Path, provider: typing.Optional[Provider] = None
    ) -> None:
        self._router = Router(root_dir=project_root, provider=provider)

    def toggle_decision(self, decision_function: types.TOOGLE_DECISION):
        """
        Decorator function for your toggle point.

        :raises InvalidDecisionFunction: This exception is thrown when either
            `when_on` and `when_off` are different types, or when any of them are booleans
        """

        @wraps(decision_function)
        def _wraps(
            when_on: types.TOGGLED_VALUE,
            when_off: types.TOGGLED_VALUE,
            context: typing.Optional[ToggleContext] = None,
        ):
            if validators.are_args_different_types(when_on, when_off):
                raise exceptions.InvalidDecisionFunction(
                    (
                        "when_on and when_off parameters must be of the same type. "
                        f"when_on parameter is {str(type(when_on))} and "
                        f"when_off parameter is {type(when_off)}"
                    )
                )

            if validators.are_args_boolean(when_on, when_off):
                raise exceptions.InvalidDecisionFunction(
                    "when_on and when_off parameters can't be boolean. "
                    "We have added this restriction to avoid a lot of if statements in your app"
                )

            if validators.are_args_invalid_functions(when_on, when_off):
                raise exceptions.InvalidDecisionFunction(
                    "when_on and when_off parameters can't be "
                    "a function which only returns a boolean. "
                    "We have added this restriction to avoid a lot of if statements in your app."
                )

            return decision_function(
                self._router.get_toggles, when_on, when_off, context
            )

        return _wraps

    def get_all_toggles(
        self,
        context: typing.Optional[ToggleContext] = None,
    ) -> typing.Dict[str, bool]:
        """
        Returns a list of all the toggles in the following format:

        ```
        {
            "my_toggle": True,
            "my_other_toggle": False,
        }
        ```

        Considerations:
        1. It only gets the toggles for the current environment,
           the one defined by the `ENVIRONMENT` env variable.
        2. Although the `context` parameter is optional, most of the
           times you will actually need to provide it, otherwise
           this function will throw an exception if you have the
           `pilot_users` or `role_based` feature types.
        """

        return self._router.get_all_toggles(context)
