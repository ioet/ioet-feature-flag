import appconfig_helper
from unittest import mock
import pytest

from ioet_feature_flag.toggle_configuration.base import ToggleConfiguration
from ioet_feature_flag.toggle_configuration.aws_appconfig_adapter import (
    AWSAppConfigAdapter,
)
from ioet_feature_flag._exceptions import ToggleNotFoundError


@pytest.fixture(autouse=True)
def _mock_aws_env_variables(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "test-region")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "test-region")
    monkeypatch.setenv("AWS_APPCONFIG_APP", "test-app")
    monkeypatch.setenv("AWS_APPCONFIG_ENV", "test-env")
    monkeypatch.setenv("AWS_APPCONFIG_PROFILE", "test-profile")


class TestAWSAppconfigAdapter:
    @mock.patch(
        "ioet_feature_flag.toggle_configuration.aws_appconfig_adapter.AppConfigHelper",
        autospec=True,
    )
    def test__returns_the_toggles_specified_in_the_config(self, appconfig_cls):
        toggles = {
            "some_toggle": {"enabled": True},
            "another_toggle": {"enabled": False},
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=toggles,
        )
        appconfig_cls.return_value = mock_appconfig

        toggle_provider: ToggleConfiguration = AWSAppConfigAdapter()
        some_toggle, another_toggle = toggle_provider.get_toggles(
            ["some_toggle", "another_toggle"]
        )

        assert some_toggle == toggles["some_toggle"]["enabled"]
        assert another_toggle == toggles["another_toggle"]["enabled"]

    @mock.patch(
        "ioet_feature_flag.toggle_configuration.aws_appconfig_adapter.AppConfigHelper",
        autospec=True,
    )
    def test__raises_an_error__if_one_of_the_toggles_does_not_exist(
        self, appconfig_cls
    ):
        toggles = {
            "some_toggle": {"enabled": True},
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=toggles,
        )
        appconfig_cls.return_value = mock_appconfig
        toggle_provider: ToggleConfiguration = AWSAppConfigAdapter()

        with pytest.raises(ToggleNotFoundError) as error:
            toggle_provider.get_toggles(["some_toggle", "another_toggle"])

        assert (
            str(error.value) == "The follwing toggles where not found: another_toggle"
        )
