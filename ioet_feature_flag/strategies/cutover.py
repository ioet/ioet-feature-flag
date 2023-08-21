import typing

from .strategy import Strategy
from ..exceptions import InvalidToggleType


class Cutover(Strategy):
    def __init__(self, enabled: bool, date: str) -> None:
        self._enabled = enabled
        self._date = date

    def is_enabled(self) -> bool:
        current_date = "?"
        if self._enabled and current_date >= self._date:
            return True
        return False


def build_cutover_type(metadata: typing.Dict) -> Cutover:
    if not metadata.get('date'):
        raise InvalidToggleType("The toggle type 'cutover' requires a 'date' attribute")
    
    # TODO: check for a valid date here

    return Cutover(
        enabled=metadata.get('enabled', False),
        date=metadata['date'],
    )
