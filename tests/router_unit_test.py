import pytest
import typing

from ioet_feature_flag.exceptions import ToggleNotFoundError
from ioet_feature_flag.router import Router


class TestGetTogglesMethod:
    @pytest.fixture(name="dependency_factory")
    def __dependency_factory(self, mocker) -> typing.Callable:
        def _factory(toggle_values: typing.Dict):
            toggle_names = toggle_values.keys()
            return {
                "provider": mocker.Mock(
                    get_toggle_list=mocker.Mock(return_value=list(toggle_names)),
                    get_toggle_attributes=mocker.Mock(
                        side_effect=[
                            toggle_values[toggle_name] for toggle_name in toggle_names
                        ]
                    ),
                )
            }

        return _factory

    def test__returns_the_toggles_specified_in_the_file_when_called_on_environment(
        self,
        dependency_factory: typing.Callable,
    ):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False},
        }

        dependencies = dependency_factory(toggle_values=toggles)
        toggle_router = Router(**dependencies)
        some_toggle, another_toggle = toggle_router.get_toggles(
            ["some_toggle", "another_toggle"]
        )

        assert some_toggle == toggles["some_toggle"]["enabled"]
        assert another_toggle == toggles["another_toggle"]["enabled"]

    def test__raises_an_error__if_one_of_the_toggles_does_not_exist(
        self,
        dependency_factory: typing.Callable,
    ):
        toggles = {"some_toggle": {"enabled": True}}
        dependencies = dependency_factory(toggle_values=toggles)
        toggle_router = Router(**dependencies)

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_router.get_toggles(["some_toggle", "another_toggle"])

        assert (
            str(error.value) == "The follwing toggles where not found: another_toggle"
        )

    def test__uses_the_toggle_context_when_it_is_provided(
        self,
        mocker,
        dependency_factory: typing.Callable,
    ):
        toggles = {"some_toggle": {"enabled": True}}
        toggle_strategy = mocker.Mock(is_enabled=mocker.Mock(return_value=True))
        toggle_context = mocker.Mock()
        mocker.patch(
            "ioet_feature_flag.router.get_toggle_strategy",
            return_value=toggle_strategy,
        )
        dependencies = dependency_factory(toggle_values=toggles)
        toggle_router = Router(**dependencies)

        toggle_router.get_toggles(["some_toggle"], toggle_context)

        toggle_strategy.is_enabled.assert_called_with(context=toggle_context)
