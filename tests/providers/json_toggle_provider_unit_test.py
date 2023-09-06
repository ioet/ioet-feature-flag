import json
import pytest
import os
import typing

from ioet_feature_flag.providers import JsonToggleProvider, Provider
from ioet_feature_flag.exceptions import ToggleNotFoundError, ToggleEnvironmentError

_TOGGLES_FILE = "/tmp/app_toggles_test.json"


@pytest.fixture(autouse=True)
def _clear_toggles_file():
    yield
    if os.path.exists(_TOGGLES_FILE):
        os.remove(_TOGGLES_FILE)


@pytest.fixture(name="add_toggles")
def _add_toggles():
    def _add(toggles: typing.Dict[str, typing.Dict[str, bool]]) -> None:
        with open(_TOGGLES_FILE, "w") as toggles_file:
            json.dump(toggles, toggles_file)

    return _add


@pytest.fixture(autouse=True)
def _del_environment(monkeypatch):
    yield
    if os.getenv("ENVIRONMENT"):
        monkeypatch.delenv("ENVIRONMENT")


class TestGetTogglesMethod:
    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test_get_toggle_list(
        self,
        environment_name: str,
        monkeypatch,
        add_toggles: typing.Callable[[typing.Dict[str, typing.Dict[str, bool]]], None],
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {
            environment_name: {
                "some_toggle": {"enabled": True},
                "another_toggle": {"enabled": False}
            }
        }
        add_toggles(toggles)

        toggle_provider: Provider = JsonToggleProvider(_TOGGLES_FILE)
        toggle_list = toggle_provider.get_toggle_list()

        assert toggle_list == ["some_toggle", "another_toggle"]

    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test_get_toggle_attribute(
        self,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
        environment_name: str,
        monkeypatch,
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {
            environment_name: {
                "some_toggle": {"enabled": True}
            }
        }
        add_toggles(toggles)
        toggle_provider: Provider = JsonToggleProvider(_TOGGLES_FILE)

        some_toggle_attributes = toggle_provider.get_toggle_attributes("some_toggle")

        assert some_toggle_attributes == {"enabled": True}

    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test_get_toggle_attribute_with_invalid_toggle(
        self,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
        environment_name: str,
        monkeypatch,
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {
            environment_name: {
                "some_toggle": {"enabled": True},
            }
        }
        add_toggles(toggles)
        toggle_provider: Provider = JsonToggleProvider(_TOGGLES_FILE)

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_provider.get_toggle_attributes("another_toggle")

        expected_message = (
            f"The toggle another_toggle was not found in the {environment_name} environment."
        )
        assert str(error.value) == expected_message

    def test_validate_no_environment(
        self,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
    ):
        toggles = {
            "some_env": {
                "some_toggle": {"enabled": True},
            }
        }
        add_toggles(toggles)

        with pytest.raises(ToggleEnvironmentError) as error:
            JsonToggleProvider(_TOGGLES_FILE)

        assert str(error.value) == "Could not retrieve toggles: Toggle environment not specified."

    @pytest.mark.parametrize("environment_name", [("production"), ("stage")])
    def test_validate_invalid_environment(
        self,
        add_toggles: typing.Callable[[typing.Dict[str, bool]], None],
        environment_name: str,
        monkeypatch,
    ):
        monkeypatch.setenv("ENVIRONMENT", environment_name)
        toggles = {
            "some_env": {
                "some_toggle": {"enabled": True},
            }
        }
        add_toggles(toggles)

        with pytest.raises(ToggleEnvironmentError) as error:
            JsonToggleProvider(_TOGGLES_FILE)

        expected_message = (
            f"The environment {environment_name} was not found "
            f"in the provided {_TOGGLES_FILE} toggles file."
        )
        assert str(error.value) == expected_message
