import pytest

import appconfig_helper
from unittest import mock
from ioet_feature_flag.exceptions import ToggleNotFoundError
from ioet_feature_flag.providers import Provider
from ioet_feature_flag.providers.aws_appconfig_toggle_provider import AWSAppConfigToggleProvider


@pytest.fixture(autouse=True)
def _mock_aws_env_variables(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "test-region")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "test-region")
    monkeypatch.setenv("AWS_APPCONFIG_APP", "test-app")
    monkeypatch.setenv("AWS_APPCONFIG_ENV", "test-env")
    monkeypatch.setenv("AWS_APPCONFIG_PROFILE", "test-profile")


class TestAWSAppConfigToggleProvider:
    @mock.patch(
        "ioet_feature_flag.providers.aws_appconfig_toggle_provider.AppConfigHelper",
        autospec=True,
    )
    def test_get_toggle_list(self, appconfig_cls):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False}
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=toggles,
        )
        appconfig_cls.return_value = mock_appconfig

        toggle_provider: Provider = AWSAppConfigToggleProvider()
        toggle_list = toggle_provider.get_toggle_list()

        assert toggle_list == ["some_toggle", "another_toggle"]

    @mock.patch(
        "ioet_feature_flag.providers.aws_appconfig_toggle_provider.AppConfigHelper",
        autospec=True,
    )
    def test_get_toggle_attribute(self, appconfig_cls):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False}
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=toggles,
        )
        appconfig_cls.return_value = mock_appconfig

        toggle_provider: Provider = AWSAppConfigToggleProvider()
        some_toggle_attributes = toggle_provider.get_toggle_attributes("some_toggle")

        assert some_toggle_attributes == {"enabled": True}

    @mock.patch(
        "ioet_feature_flag.providers.aws_appconfig_toggle_provider.AppConfigHelper",
        autospec=True,
    )
    def test_get_toggle_attribute_with_invalid_toggle(self, appconfig_cls):
        toggles = {
            "some_toggle": {"enabled": True},
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=toggles,
        )
        appconfig_cls.return_value = mock_appconfig
        toggle_provider: Provider = AWSAppConfigToggleProvider()

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_provider.get_toggle_attributes("another_toggle")

        expected_message = "The toggle another_toggle was not found in the test-env environment."
        assert str(error.value) == expected_message
