import json
import pytest
import typing
import requests

from ioet_feature_flag.providers import JsonGitRemoteProvider, Provider
from ioet_feature_flag.exceptions import (
    ToggleNotFoundError,
    InvalidToggleFileFormat,
)


@pytest.fixture(name="mock_request")
def _mock_request(mocker):
    def _add(toggles_text: str) -> mocker.Mock:
        mocked_response = mocker.create_autospec(
            requests.Response,
            text=toggles_text,
        )
        return mocker.patch("requests.request", return_value=mocked_response)

    return _add


class TestJsonGitRemoteProvider:
    def test_get_toggle_list(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False},
        }
        mock_request(json.dumps(toggles))
        toggle_provider: Provider = JsonGitRemoteProvider(
            project_id="test",
            environment="test",
        )

        toggle_list = toggle_provider.get_toggle_list()
        assert toggle_list == ["some_toggle", "another_toggle"]

    def test_get_toggle_attribute(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        toggles = {"some_toggle": {"enabled": True}}
        mock_request(json.dumps(toggles))
        toggle_provider: Provider = JsonGitRemoteProvider(
            project_id="test",
            environment="test",
        )

        some_toggle_attributes = toggle_provider.get_toggle_attributes("some_toggle")
        assert some_toggle_attributes == {"enabled": True}

    def test_get_toggle_attribute_with_invalid_toggle(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        toggles = {
            "some_toggle": {"enabled": True},
        }
        mock_request(json.dumps(toggles))
        toggle_provider: Provider = JsonGitRemoteProvider(
            project_id="test",
            environment="test",
        )

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_provider.get_toggle_attributes("another_toggle")

        expected_message = "The toggle another_toggle was not found."
        assert str(error.value) == expected_message

    def test_load_toggles_from_file_raises_error_when_file_format_invalid(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        invalid_text = "some invalid text"
        mock_request(invalid_text)

        with pytest.raises(InvalidToggleFileFormat) as error:
            provider = JsonGitRemoteProvider(
                project_id="test",
                environment="test",
            )
            provider.get_toggle_list()

        expected_message = "The provided file doesn't have a valid JSON format."
        assert str(error.value) == expected_message

    def test_load_toggles_from_file_raises_error_when_remote_returns_http_error_code(
        self, mocker
    ):
        mocker.patch("requests.Response.raise_for_status", side_effect=requests.HTTPError)

        with pytest.raises(InvalidToggleFileFormat) as error:
            provider = JsonGitRemoteProvider(
                project_id="test",
                environment="test",
            )
            provider.get_toggle_list()

        expected_message = "Unable to load toggles file from remote"
        assert expected_message in str(error.value)

    def test_load_toggles_from_file_raises_error_when_file_contents_is_empty(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        mock_request("")

        with pytest.raises(InvalidToggleFileFormat) as error:
            provider = JsonGitRemoteProvider(
                project_id="test",
                environment="test",
            )
            provider.get_toggle_list()

        expected_message = "The provided file is empty."
        assert str(error.value) == expected_message

    def test_load_toggles_request_called_with_right_parameters(
        self,
        mock_request: typing.Callable[[str], None],
    ):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False},
        }
        patched_request = mock_request(json.dumps(toggles))
        toggle_provider: Provider = JsonGitRemoteProvider(
            base_url="https://test-remote.com/test-user/test-repo/main/",
            project_id="test-project",
            environment="test-env",
        )

        toggle_list = toggle_provider.get_toggle_list()

        patched_request.assert_called_with(
            method="GET",
            url="https://test-remote.com/test-user/test-repo/main/test-project/test-env.json",
            headers=None,
        )
        assert toggle_list == ["some_toggle", "another_toggle"]
