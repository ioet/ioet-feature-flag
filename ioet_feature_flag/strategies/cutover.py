import datetime
import typing

from .strategy import Strategy
from ..exceptions import InvalidToggleAttribute, MissingToggleAttributes


class Cutover(Strategy):
    def __init__(self, enabled: bool, date: datetime.datetime) -> None:
        self._enabled = enabled
        self._date = date

    @classmethod
    def from_metadata(cls, metadata: typing.Dict) -> "Cutover":
        if not metadata.get("date"):
            raise MissingToggleAttributes("The toggle type 'cutover' requires a 'date' attribute")

        try:
            date = datetime.datetime.strptime(metadata.get("date"), "%Y-%m-%d %H:%M")
        except ValueError as e:
            raise InvalidToggleAttribute(
                f"The provided date for the toggle is not valid: {str(e)}."
            )

        return cls(
            enabled=metadata.get('enabled', False),
            date=date,
        )

    def is_enabled(self) -> bool:
        current_date = datetime.datetime.utcnow()
        if self._enabled and current_date >= self._date:
            return True
        return False
