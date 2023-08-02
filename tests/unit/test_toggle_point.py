import pytest

from ioet_feature_flag import TogglePoint, InvalidDecisionParameters


class TestTogglePoint:
    @pytest.mark.parametrize(
        "flag_value, path_executed",
        [
            (True, "first"),
            (False, "second"),
        ],
    )
    def test__toggles_behaviour_on_flag_status(
        self,
        mocker,
        flag_value: bool,
        path_executed: str,
    ):
        toggle_router_mock = mocker.Mock(
            return_value=mocker.Mock(return_value=flag_value)
        )
        behaviour_path_mocks = {"first": mocker.Mock(), "second": mocker.Mock()}
        toggle_point = TogglePoint(toggle_router=toggle_router_mock)

        result = toggle_point.toggle(
            when_on=behaviour_path_mocks["first"],
            when_off=behaviour_path_mocks["second"],
        )

        assert behaviour_path_mocks[path_executed] == result

    def test__calls_decorated_function_with_toggle_object_and_paths(self, mocker):
        function_to_decorate = mocker.Mock()
        when_on = mocker.Mock()
        when_off = mocker.Mock()
        toggle_router_mock = mocker.Mock(return_value=mocker.Mock(return_value=True))
        toggle_point = TogglePoint(toggle_router=toggle_router_mock)

        toggle_point(function_to_decorate)(when_on=when_on, when_off=when_off)

        function_to_decorate.assert_called_with(
            toggle_point=toggle_point, when_on=when_on, when_off=when_off
        )

    def test__raises_an_error_when_toggle_values_are_from_different_types(self, mocker):
        function_to_decorate = mocker.Mock()
        when_on = "abc"
        when_off = 123
        toggle_router_mock = mocker.Mock(return_value=mocker.Mock(return_value=True))
        toggle_point = TogglePoint(toggle_router=toggle_router_mock)

        with pytest.raises(InvalidDecisionParameters) as error:
            toggle_point(function_to_decorate)(when_on=when_on, when_off=when_off)

        assert str(error.value) == (
            "when_on and when_off parameters must be of the same type. "
            "when_on parameter is <class 'str'> and when_off parameter is <class 'int'>"
        )
