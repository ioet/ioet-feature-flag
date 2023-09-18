import pytest

from ioet_feature_flag.strategies import PilotUsers
from ioet_feature_flag.exceptions import MissingToggleAttributes
from ioet_feature_flag.toggle_context import ToggleContext


class TestCutoverStrategy:
    @pytest.mark.parametrize(
        "is_enabled, current_user, allowed_users, expected_result, expected_exception",
        [
            (True, 'allowed_user', '', False, MissingToggleAttributes),
            (True, 'allowed_user', 'allowed_user', True, None),
            (True, 'allowed_user', 'allowed_user,another_user', True, None),
            (False, 'allowed_user', 'allowed_user', False, None),
            (False, 'allowed_user', 'allowed_user,another_user', False, None),
        ]
    )
    def test__returns_toggles_specified_in_attributes(
        self,
        is_enabled,
        current_user,
        allowed_users,
        expected_result,
        expected_exception,
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "pilot_users",
            "allowed_users": allowed_users,
        }
        toggle_context = ToggleContext(username=current_user, role="default")
        if expected_exception:
            with pytest.raises(expected_exception):
                PilotUsers.from_attributes(attributes)
        else:
            cutover_strategy = PilotUsers.from_attributes(attributes)
            assert cutover_strategy.is_enabled(context=toggle_context) == expected_result
