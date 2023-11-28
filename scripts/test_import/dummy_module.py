from pathlib import Path
import ioet_feature_flag

toggles = ioet_feature_flag.Toggles(project_root=Path(__file__).parent)


@toggles.toggle_decision
def dummy_decision(get_toggles, when_on, when_off, context=None):
    is_enabled = get_toggles(["dummy-flag"], context)
    if is_enabled:
        return when_on
    return when_off


@toggles.toggle_decision
def dummy_decision_when_off(get_toggles, when_on, when_off, context=None):
    is_enabled = get_toggles(["disabled-flag"], context)
    if is_enabled:
        return when_on
    return when_off


@toggles.toggle_decision
def dummy_decision_user(get_toggles, when_on, when_off, context=None):
    is_enabled = get_toggles(["user-dummy-flag"], context)
    if is_enabled:
        return when_on
    return when_off


def get_name():
    return dummy_decision(
        when_on="name-a",
        when_off="name-b",
    )


def get_name_b():
    return dummy_decision_when_off(
        when_on="name-a",
        when_off="name-b",
    )


def get_name_user():
    return dummy_decision_user(
        when_on="name-a",
        when_off="name-b",
        context=ioet_feature_flag.ToggleContext(
            username="test_user",
            role="",
        ),
    )
