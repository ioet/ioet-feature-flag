import pytest
import typing
from unittest import mock

from ioet_featureflag import FeatureFlags
from ioet_featureflag.providers import MockAppconfig

@pytest.mark.parametrize(
    "mock_config, feature_name, expected_result",
    [
        (
            {"test_feature": True},
            "test_feature",
            True,
        ),
        (
            {"test_feature": False},
            "test_feature",
            False,
        ),
        (
            {"test_feature": True},
            "another_feature",
            False,
        ),
    ]
)
def test_is_enabled(
    mock_config: typing.Dict,
    feature_name: str,
    expected_result: bool,
):
    feature_flags = FeatureFlags(provider=MockAppconfig(mock_config))
    assert feature_flags.is_enabled(feature_name) == expected_result


def test_enable_feature():
    feature_flags = FeatureFlags(provider=MockAppconfig({}))
    assert not feature_flags.is_enabled("test_feature")
    feature_flags.enable_feature("test_feature")
    assert feature_flags.is_enabled("test_feature")


def test_disable_feature():
    feature_flags = FeatureFlags(
        provider=MockAppconfig(
            config={"test_feature": True},
        ),
    )
    assert feature_flags.is_enabled("test_feature")
    feature_flags.disable_feature("test_feature")
    assert not feature_flags.is_enabled("test_feature")


@pytest.mark.parametrize(
    "feature_enabled",
    [True, False]
)
def test_on_off(feature_enabled):
    feature_flags = FeatureFlags(
        provider=MockAppconfig(
            config={"test_feature": feature_enabled},
        ),
    )

    mock_old_feature = mock.Mock()
    mock_new_feature = mock.Mock()

    @feature_flags.off("test_feature")
    def _old_feature():
        mock_old_feature()

    @feature_flags.on("test_feature")
    def _new_feature():
        mock_new_feature()

    def wrapper():
        _old_feature()
        _new_feature()
    
    wrapper()

    if feature_enabled:
        mock_old_feature.assert_not_called()
        mock_new_feature.assert_called()
    else:
        mock_old_feature.assert_called()
        mock_new_feature.assert_not_called()
