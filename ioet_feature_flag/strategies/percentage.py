import enum
import random
import typing

from ..exceptions import InvalidToggleAttribute, MissingToggleAttributes, MissingToggleContext
from ..toggle_context import ToggleContext
from .strategy import Strategy


class UserPercentage(Strategy):
    class FeaturePath(enum.Enum):
        DISABLED = 0
        ENABLED = 1

    def __init__(self, percentage: float, salt: str) -> None:
        self._percentage = percentage
        self._salt = salt

    def is_enabled(self, context: typing.Optional[ToggleContext] = None) -> bool:
        self._raise_for_missing_context(context)

        success_probability = self._percentage
        failure_probability = 100 - self._percentage

        seed = context.username + self._salt
        random.seed(seed)
        feature_path = random.choices(
            [self.FeaturePath.ENABLED, self.FeaturePath.DISABLED],
            weights=[success_probability, failure_probability],
        )

        return bool(feature_path[0].value)

    def _raise_for_missing_context(self, context: typing.Optional[ToggleContext]) -> None:
        if not context:
            raise MissingToggleContext("Toggle context is required to compute toggle's state")

    @classmethod
    def from_attributes(cls, attributes: typing.Dict) -> "UserPercentage":
        try:
            percentage = attributes["percentage"]
            cls._validate_percentage_value(percentage)
            salt = attributes["salt"]
            cls._validate_salt_value(salt)
            return cls(percentage, salt)
        except KeyError as key_error:
            error_message = f"You must provide a {key_error.args[0]} value"
            raise MissingToggleAttributes(error_message) from KeyError

    @classmethod
    def _validate_percentage_value(cls, percentage: typing.Any) -> None:
        if not isinstance(percentage, float):
            raise InvalidToggleAttribute(
                f"The percentage provided has incompatible type ({type(percentage).__name__}),"
                " expected float"
            )
        if cls._is_percentage_out_of_range(percentage):
            raise InvalidToggleAttribute(
                f"The percentage provided ({percentage:.2f}) is outside the allowed range [0-100]"
            )

    @classmethod
    def _is_percentage_out_of_range(cls, percentage: float) -> bool:
        return (percentage < 0) or (percentage > 100)

    @classmethod
    def _validate_salt_value(cls, salt) -> None:
        if not isinstance(salt, str):
            raise InvalidToggleAttribute(
                f"The salt value provided has incompatible type ({type(salt).__name__}), "
                "expected str"
            )
