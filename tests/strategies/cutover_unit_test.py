import pytest
from freezegun import freeze_time

from ioet_feature_flag.strategies import Cutover
from ioet_feature_flag.exceptions import InvalidToggleAttribute, MissingToggleAttributes


class TestCutoverStrategy:
    @pytest.mark.parametrize(
        "is_enabled, date, expected_result, expected_exception",
        [
            (True, '2023-08-20 10:00', True, None),
            (True, '2023-08-20 17:00', False, None),
            (True, '2023-08-21 10:00', False, None),
            (False, '2023-08-20 10:00', False, None),
            (True, '2023-08-20', True, InvalidToggleAttribute),
            (True, 'invalid date', True, InvalidToggleAttribute),
            (True, '2023/08/20 08:00', True, InvalidToggleAttribute),
            (True, None, True, MissingToggleAttributes),
        ]
    )
    @freeze_time("2023-08-20 14:00:00", tz_offset=-4)
    def test__returns_toggles_specified_in_attributes(
        self,
        is_enabled,
        date,
        expected_result,
        expected_exception,
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "cutover",
            "date": date,
        }
        if expected_exception:
            with pytest.raises(expected_exception):
                Cutover.from_attributes(attributes)
        else:
            cutover_strategy = Cutover.from_attributes(attributes)
            assert cutover_strategy.is_enabled() == expected_result
