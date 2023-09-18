import yaml
import pytest
import os
import typing

from ioet_feature_flag.providers import YamlToggleProvider
from ioet_feature_flag.exceptions import ToggleNotFoundError
from ioet_feature_flag.router import Router

_TOGGLES_FILE = "/tmp/app_toggles_test.yaml"


@pytest.fixture(autouse=True)
def _clear_toggles_file():
    yield
    if os.path.exists(_TOGGLES_FILE):
        os.remove(_TOGGLES_FILE)


@pytest.fixture(name="add_toggles")
def _add_toggles():
    def _add(toggles: typing.Dict[str, typing.Dict[str, bool]]) -> None:
        with open(_TOGGLES_FILE, "w") as toggles_file:
            yaml.dump(toggles, toggles_file)

    return _add


@pytest.fixture(autouse=True)
def _del_environment(monkeypatch):
    yield
    if os.getenv("ENVIRONMENT"):
        monkeypatch.delenv("ENVIRONMENT")


class TestGetTogglesMethod:
    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test__returns_the_toggles_specified_in_the_file_when_called_on_environment(
        self,
        environment_name: str,
        monkeypatch,
        add_toggles: typing.Callable[[typing.Dict[str, typing.Dict[str, bool]]], None],
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {
            environment_name: {
                "some_toggle": {"enabled": True},
                "another_toggle": {"enabled": False},
            }
        }
        add_toggles(toggles)

        toggle_provider = YamlToggleProvider(_TOGGLES_FILE)
        toggle_router = Router(toggle_provider)
        some_toggle, another_toggle = toggle_router.get_toggles(
            ["some_toggle", "another_toggle"]
        )

        assert some_toggle == toggles[environment_name]["some_toggle"]["enabled"]
        assert another_toggle == toggles[environment_name]["another_toggle"]["enabled"]

    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test__raises_an_error__if_one_of_the_toggles_does_not_exist(
        self,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
        environment_name: str,
        monkeypatch,
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {environment_name: {"some_toggle": {"enabled": True}}}
        add_toggles(toggles)
        toggle_provider = YamlToggleProvider(_TOGGLES_FILE)
        toggle_router = Router(toggle_provider)

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_router.get_toggles(["some_toggle", "another_toggle"])

        assert (
            str(error.value) == "The follwing toggles where not found: another_toggle"
        )

    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test__uses_the_toggle_context_when_it_is_provided(
        self,
        mocker,
        monkeypatch,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
        environment_name: str,
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {environment_name: {"some_toggle": {"enabled": True}}}
        add_toggles(toggles)
        toggle_strategy = mocker.Mock(is_enabled=mocker.Mock(return_value=True))
        toggle_context = mocker.Mock()
        mocker.patch(
            "ioet_feature_flag.router.get_toggle_strategy",
            return_value=toggle_strategy,
        )
        toggle_provider = YamlToggleProvider(_TOGGLES_FILE)
        toggle_router = Router(toggle_provider)

        toggle_router.get_toggles(["some_toggle"], toggle_context)

        toggle_strategy.is_enabled.assert_called_with(context=toggle_context)