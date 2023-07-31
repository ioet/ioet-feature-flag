import pytest

from ioet_feature_flag.feature_router import FeatureRouter
from ioet_feature_flag.feature_router import TogglePoint


class TestFeatureRouter:
    def test_set_feature_toggle_returns_updated_toggles(self, mocker):
        expected_result = {"flag_1": True, "flag_2": False}
        feature_repository_attrs = {
            "get_flags.return_value": {"flag_1": True},
            "set_flag.return_value": expected_result,
        }
        feature_repository_mock = mocker.Mock()
        feature_repository_mock.configure_mock(**feature_repository_attrs)
        mocker.patch(
            "ioet_feature_flag.feature_router.AWSAppConfigAdapter",
            return_value=feature_repository_mock,
        )
        router = FeatureRouter()

        router.set_feature_toggle("flag_2", False)

        feature_repository_mock.set_flag.assert_called_once_with("flag_2", False)
        assert expected_result == router.feature_flags

    @pytest.mark.parametrize(
        "first_flag_state, second_flag_state, expected_state",
        [
            (True, True, True),
            (True, False, False),
        ],
    )
    def test_are_features_enabled_returns_feature_status(
        self,
        monkeypatch,
        first_flag_state: bool,
        second_flag_state: bool,
        expected_state: bool,
    ):
        feature_repository_flags = {
            "flag_1": first_flag_state,
            "flag_2": second_flag_state,
        }
        router = FeatureRouter()
        monkeypatch.setattr(router, "feature_flags", feature_repository_flags)

        actual_state = router.are_features_enabled("flag_1", "flag_2")

        assert expected_state == actual_state


class TestTogglePoint:
    @pytest.mark.parametrize(
        "flag_value, path_executed",
        [
            (True, "first"),
            (False, "second"),
        ],
    )
    def test_toggle_point_toggles_behaviour_on_flag_status(
        self,
        mocker,
        flag_value: bool,
        path_executed: str,
    ):
        router_repository_attrs = {"are_features_enabled.return_value": flag_value}
        router_repository_mock = mocker.Mock()
        router_repository_mock.configure_mock(**router_repository_attrs)
        behaviour_path_mocks = {"first": mocker.Mock(), "second": mocker.Mock()}
        toggle_point = TogglePoint(
            toggle_router=router_repository_mock, feature_names="flag"
        )

        toggle_point.toggle(
            path_when_enabled=behaviour_path_mocks["first"],
            path_when_disabled=behaviour_path_mocks["second"],
        )

        behaviour_path_mocks[path_executed].assert_called_once()
