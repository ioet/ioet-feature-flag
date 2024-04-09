import pytest

from ioet_feature_flag.exceptions import InvalidToggleType
from ioet_feature_flag.strategies import (
    Cutover,
    PilotUsers,
    RoleBased,
    Static,
    UserPercentage,
    get_toggle_strategy,
)


@pytest.mark.parametrize(
    "attributes, expected_result, expected_exception",
    [
        ({"type": "static"}, Static, None),
        ({"type": "cutover", "date": "2023-08-21 08:00"}, Cutover, None),
        ({"type": "pilot_users", "allowed_users": ["test"]}, PilotUsers, None),
        ({"type": "role_based", "roles": ["tester"]}, RoleBased, None),
        ({"type": "percentage", "percentage": 20.0, "salt": "FF-43"}, UserPercentage, None),
        ({"type": "non_existent_type"}, None, InvalidToggleType),
    ],
)
def test_get_toggle_strategy(attributes, expected_result, expected_exception):
    attributes["enabled"] = True
    if expected_exception:
        with pytest.raises(expected_exception):
            get_toggle_strategy(attributes)
    else:
        strategy = get_toggle_strategy(attributes)
        assert isinstance(strategy, expected_result)
