import pytest

from ioet_feature_flag import Toggles
from ioet_feature_flag.exceptions import InvalidDecisionFunction
from ioet_feature_flag.router import Router


class TestTogglesDecisionMethod:
    @pytest.mark.parametrize("uses_context", [True, False])
    def test__injects_the_method_to_retrieve_toggles_to_the_decision_method(
        self, mocker, uses_context: bool
    ):
        provider = mocker.Mock()
        when_on = mocker.Mock()
        when_off = mocker.Mock()
        get_toggles = mocker.Mock()
        router = mocker.create_autospec(Router, get_toggles=get_toggles)
        mocker.patch(
            "ioet_feature_flag.toggles.Router",
            return_value=router,
        )
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider, project_root=mocker.Mock())
        toggle_context = mocker.Mock() if uses_context else None

        decision = toggles.toggle_decision(decision_function)
        decided_value = decision(
            when_on=when_on, when_off=when_off, context=toggle_context
        )

        decision_function.assert_called_with(
            router.get_toggles, when_on, when_off, toggle_context
        )
        assert decided_value == when_on

    def test__raises_an_error_when_toggle_values_are_from_different_types(self, mocker):
        provider = mocker.Mock()
        router = mocker.Mock()
        mocker.patch(
            "ioet_feature_flag.toggles.Router",
            return_value=router,
        )
        when_on = 1
        when_off = "string"
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider, project_root=mocker.Mock())

        with pytest.raises(InvalidDecisionFunction) as error:
            toggles.toggle_decision(decision_function)(
                when_on=when_on, when_off=when_off
            )

        assert str(error.value) == (
            "when_on and when_off parameters must be of the same type. "
            "when_on parameter is <class 'int'> and when_off parameter is <class 'str'>"
        )

    def test__raises_an_error_when_toggle_values_are_boolean(self, mocker):
        provider = mocker.Mock()
        router = mocker.Mock()
        mocker.patch(
            "ioet_feature_flag.toggles.Router",
            return_value=router,
        )
        when_on = True
        when_off = False
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider, project_root=mocker.Mock())

        with pytest.raises(InvalidDecisionFunction) as error:
            toggles.toggle_decision(decision_function)(
                when_on=when_on, when_off=when_off
            )

        assert str(error.value) == (
            "when_on and when_off parameters can't be boolean. "
            "We have added this restriction to avoid a lot of if statements in your app"
        )

    def test__raises_an_error_when_toggle_values_are_functions_that_return_boolean(self, mocker):
        provider = mocker.Mock()
        router = mocker.Mock()
        mocker.patch(
            "ioet_feature_flag.toggles.Router",
            return_value=router,
        )

        def _dummy_when_on():
            return True

        def _dummy_when_off():
            return False

        when_on = _dummy_when_on
        when_off = _dummy_when_off
        decision_function = mocker.Mock(return_value=when_on)
        toggles = Toggles(provider=provider, project_root=mocker.Mock())

        with pytest.raises(InvalidDecisionFunction) as error:
            toggles.toggle_decision(decision_function)(
                when_on=when_on, when_off=when_off
            )

        assert str(error.value) == (
            "when_on and when_off parameters can't be "
            "a function which only returns a boolean. "
            "We have added this restriction to avoid a lot of if statements in your app."
        )
