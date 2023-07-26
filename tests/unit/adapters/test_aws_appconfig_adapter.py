import pytest
import appconfig_helper
from unittest import mock

from ioet_feature_flag.adapters.aws_appconfig_adapter import AWSAppConfigAdapter


class TestAWSAppconfigAdapter:
    @mock.patch("ioet_feature_flag.adapters.aws_appconfig_adapter.AppConfigHelper", autospec=True)
    def test_get_flags(
        self, appconfig_cls, monkeypatch
    ):
        monkeypatch.setenv('AWS_REGION', 'test-region')
        monkeypatch.setenv('AWS_DEFAULT_REGION', 'test-region')
        monkeypatch.setenv('AWS_APPCONFIG_APP', 'test-app')
        monkeypatch.setenv('AWS_APPCONFIG_ENV', 'test-env')
        monkeypatch.setenv('AWS_APPCONFIG_PROFILE', 'test-profile')
        expected_flags = {
            "flag_1": {
                "enabled": True,
            },
            "flag_2": {
                "enabled": False,
            },
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=expected_flags,
        )
        appconfig_cls.return_value = mock_appconfig
        actual_flags = AWSAppConfigAdapter().get_flags()

        assert expected_flags == actual_flags

    @mock.patch("ioet_feature_flag.adapters.aws_appconfig_adapter.AppConfigHelper", autospec=True)
    def test_set_flag(
        self, appconfig_cls, monkeypatch
    ):
        monkeypatch.setenv('AWS_REGION', 'test-region')
        monkeypatch.setenv('AWS_DEFAULT_REGION', 'test-region')
        monkeypatch.setenv('AWS_APPCONFIG_APP', 'test-app')
        monkeypatch.setenv('AWS_APPCONFIG_ENV', 'test-env')
        monkeypatch.setenv('AWS_APPCONFIG_PROFILE', 'test-profile')
        outdated_flags = {
            "flag_1":{
                "enabled": True,
            },
            "flag_2": {
                "enabled": False,
            },
        }
        expected_flags = {
            "flag_1": {
                "enabled": False,
            },
            "flag_2": {
                "enabled": False,
            },
        }
        mock_appconfig = mock.create_autospec(
            appconfig_helper.AppConfigHelper,
            config=outdated_flags,
        )
        appconfig_cls.return_value = mock_appconfig
        actual_flags = AWSAppConfigAdapter().set_flag("flag_1", False)

        assert expected_flags == actual_flags
