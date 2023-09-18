import pytest


from ioet_feature_flag.strategies import get_toggle_strategy
from ioet_feature_flag.strategies import Static, Cutover, PilotUsers
from ioet_feature_flag.exceptions import InvalidToggleType


@pytest.mark.parametrize(
    "attributes, expected_result, expected_exception",
    [
        ({"type": "static"}, Static, None),
        ({"type": "cutover", "date": "2023-08-21 08:00"}, Cutover, None),
        ({"type": "pilot_users", "allowed_users": "test"}, PilotUsers, None),
        ({"type": "non_existent_type"}, None, InvalidToggleType),
    ]
)
def test_get_toggle_strategy(attributes, expected_result, expected_exception):
    attributes["enabled"] = True
    if expected_exception:
        with pytest.raises(expected_exception):
            get_toggle_strategy(attributes)
    else:
        strategy = get_toggle_strategy(attributes)
        assert isinstance(strategy, expected_result)
