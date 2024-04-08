import re
import typing

import pytest

from ioet_feature_flag import exceptions, strategies


class TestPercentageStrategy:
    @pytest.fixture
    def dependency_factory(self, mocker) -> typing.Callable[..., typing.Dict]:
        def factory(**context_attributes: typing.Dict) -> typing.Dict[str, typing.Any]:
            return {
                "toggle_context": mocker.Mock(
                    username=context_attributes.get("username", "default_user"),
                    role=context_attributes.get("role", "default"),
                )
            }

        return factory

    @pytest.fixture
    def flag_definition_factory(self) -> typing.Callable[..., typing.Dict]:
        def factory(percentage: float, salt: str = "FF-43") -> typing.Dict:
            return {
                "type": "percentage",
                "percentage": percentage,
                "salt": salt,
            }

        return factory

    def test__returns_a_percentage_stategy_instance(
        self, flag_definition_factory: typing.Callable[..., typing.Dict]
    ) -> None:
        user_percentage = 20.0
        toggle_properties = flag_definition_factory(user_percentage)

        percentage_strategy = strategies.UserPercentage.from_attributes(toggle_properties)

        assert isinstance(percentage_strategy, strategies.UserPercentage)
        assert isinstance(percentage_strategy, strategies.Strategy)

    @pytest.mark.parametrize("call_number", [100, 1000], ids=("100 calls", "1000 calls"))
    @pytest.mark.parametrize(
        "user, salt, is_enabled",
        [("user_a@example.com", "FF-400", True), ("user_b@example.com", "PER-100", False)],
        ids=("enabled_path", "disabled_path"),
    )
    def test__given_a_user_and_a_flag__then_feature_value_is_preserved(
        self,
        flag_definition_factory: typing.Callable[..., typing.Dict],
        dependency_factory: typing.Callable[..., typing.Dict],
        call_number: int,
        user: str,
        salt: str,
        is_enabled: bool,
    ) -> None:
        dependencies = dependency_factory(username=user)
        user_percentage = 20.0
        toggle_properties = flag_definition_factory(user_percentage, salt)
        percentage_strategy = strategies.UserPercentage.from_attributes(toggle_properties)

        is_feature_enabled_for_user = (
            percentage_strategy.is_enabled(dependencies["toggle_context"]) == is_enabled
            for _ in range(call_number)
        )

        assert all(is_feature_enabled_for_user)

    @pytest.mark.parametrize(
        "missing_attribute", ["percentage", "salt"], ids=("percentage_missing", "salt_missing")
    )
    def test__when_toggle_attributes_are_missing__then_error_is_raised(
        self,
        flag_definition_factory: typing.Callable[..., typing.Dict],
        missing_attribute: str,
    ) -> None:
        user_percentage = 10.0
        expected_error_message = f"You must provide a {missing_attribute} value"
        toggle_properties = flag_definition_factory(user_percentage)
        toggle_properties.pop(missing_attribute)

        with pytest.raises(exceptions.MissingToggleAttributes, match=expected_error_message):
            strategies.UserPercentage.from_attributes(toggle_properties)

    @pytest.mark.parametrize(
        argnames="invalid_percentage_value, invalid_salt_value, error_message",
        argvalues=[
            (-13.2, None, "The percentage provided (-13.20) is outside the allowed range [0-100]"),
            (100.01, None, "The percentage provided (100.01) is outside the allowed range [0-100]"),
            (
                "str_percentage",
                None,
                "The percentage provided has incompatible type (str), expected float",
            ),
            (None, True, "The salt value provided has incompatible type (bool), expected str"),
        ],
        ids=("negative_percentage", "exceeded_percentage", "string_percentage", "boolean_salt"),
    )
    def test__when_attribute_has_invalid_value__then_error_is_raised(
        self,
        flag_definition_factory: typing.Callable[..., typing.Dict],
        invalid_percentage_value: typing.Any,
        invalid_salt_value: typing.Any,
        error_message: str,
    ) -> None:
        user_percentage = 10.0
        salt = "ff-43"
        toggle_properties = flag_definition_factory(
            **{
                "percentage": invalid_percentage_value
                if invalid_percentage_value
                else user_percentage,
                "salt": invalid_salt_value if invalid_salt_value else salt,
            }
        )

        with pytest.raises(exceptions.InvalidToggleAttribute, match=re.escape(error_message)):
            strategies.UserPercentage.from_attributes(toggle_properties)

    def test__when_toggle_context_is_not_provided__then_error_is_raised(
        self,
        flag_definition_factory: typing.Callable[..., typing.Dict],
    ):
        expected_error_message = "Toggle context is required to compute toggle's state"
        user_percentage = 10.0
        toggle_properties = flag_definition_factory(user_percentage)
        percentage_strategy = strategies.UserPercentage.from_attributes(toggle_properties)

        with pytest.raises(exceptions.MissingToggleContext, match=expected_error_message):
            percentage_strategy.is_enabled()
