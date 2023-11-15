import typing

import pytest

from ioet_feature_flag.strategies import PilotUsers
from ioet_feature_flag.exceptions import (
    MissingToggleAttributes,
    InvalidToggleAttribute,
    MissingToggleContext,
)


class TestPilotUsersStrategy:
    @pytest.fixture
    def dependency_factory(self, mocker):
        def _factory(**context_attributes: typing.Dict):
            return {
                "toggle_context": mocker.Mock(
                    username=context_attributes.get("username", "default_user"),
                    role=context_attributes.get("role", "default"),
                )
            }

        return _factory

    @pytest.mark.parametrize(
        "is_enabled, current_user, allowed_users, expected_result, expected_exception",
        [
            (True, "allowed_user", "", False, MissingToggleAttributes),
            (
                True,
                "allowed_user",
                "test_user, test_another_user",
                False,
                InvalidToggleAttribute,
            ),
            (True, "allowed_user", ["allowed_user"], True, None),
            (True, "allowed_user", ["allowed_user", "another_user"], True, None),
            (True, "allowed_user", [" allowed_user", "another_user"], True, None),
            (True, "allowed_user", ["allowed_user ", "another_user"], True, None),
            (False, "allowed_user", ["allowed_user"], False, None),
            (False, "allowed_user", ["allowed_user", "another_user"], False, None),
            (True, "not_allowed_user", ["allowed_user"], False, None),
            (True, "not_allowed_user", ["allowed_user", "another_user"], False, None),
            (False, "not_allowed_user", ["allowed_user"], False, None),
            (False, "not_allowed_user", ["allowed_user", "another_user"], False, None),
        ],
    )
    def test__returns_toggles_specified_in_attributes(
        self,
        is_enabled: bool,
        current_user: str,
        allowed_users: typing.Any,
        expected_result: bool,
        expected_exception: typing.Any,
        dependency_factory: typing.Callable,
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "pilot_users",
            "allowed_users": allowed_users,
        }
        toggle_context = dependency_factory(username=current_user)["toggle_context"]

        if expected_exception:
            with pytest.raises(expected_exception):
                PilotUsers.from_attributes(attributes)
        else:
            pilot_users_strategy = PilotUsers.from_attributes(attributes)
            assert (
                pilot_users_strategy.is_enabled(context=toggle_context)
                == expected_result
            )

    def test__raises_an_exception__when_toggle_context_was_not_provided(
        self,
    ):
        expected_error_message = "Toggle context is required to compute toggle's state"
        attributes = {
            "enabled": True,
            "type": "pilot_users",
            "allowed_users": ["allUsers"],
        }
        pilot_users_strategy = PilotUsers.from_attributes(attributes)

        with pytest.raises(MissingToggleContext, match=expected_error_message):
            pilot_users_strategy.is_enabled()
