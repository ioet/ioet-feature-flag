import typing

import pytest

from ioet_feature_flag.strategies import RoleBased
from ioet_feature_flag.exceptions import MissingToggleAttributes, InvalidToggleAttribute


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
        "is_enabled, current_role, allowed_roles, expected_result",
        [
            (True, "allowed_role", ["allowed_role"], True),
            (True, "not_allowed_role", ["allowed_role", "another_role"], False),
            (True, "allowed_role", [" allowed_role", "another_role"], True),
            (True, "another_role", ["allowed_role ", "another_role "], True),
            (False, "allowed_role", ["allowed_role", "another_role"], False),
            (False, "not_allowed_role", ["allowed_role", "another_role"], False),
        ],
    )
    def test__returns_toggle_value_according_to_attributes(
        self,
        is_enabled: bool,
        current_role: str,
        allowed_roles: str,
        expected_result: bool,
        dependency_factory: typing.Callable,
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "role_based",
            "roles": allowed_roles
        }
        toggle_context = dependency_factory(role=current_role)["toggle_context"]

        role_based_strategy = RoleBased.from_attributes(attributes)
        assert (
            role_based_strategy.is_enabled(context=toggle_context)
            == expected_result
        )

    @pytest.mark.parametrize(
        "is_enabled, current_role, allowed_roles, expected_exception",
        [
            (True, "allowed_user", "", MissingToggleAttributes),
            (True, "allowed_user", "test_user, test_another_user", InvalidToggleAttribute),
        ]
    )
    def test__raises_an_error__when_attributes_are_not_formatted_correctly(
        self,
        is_enabled: bool,
        current_role: str,
        allowed_roles: str,
        dependency_factory: typing.Callable,
        expected_exception: typing.Any
    ):
        attributes = {
            "enabled": is_enabled,
            "type": "role_based",
            "roles": allowed_roles
        }

        with pytest.raises(expected_exception):
            RoleBased.from_attributes(attributes)
