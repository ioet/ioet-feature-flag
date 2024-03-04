import ioet_feature_flag

import typing

provider = ioet_feature_flag.YamlToggleProvider('./feature_toggles/feature-toggles.yaml')
toggles = ioet_feature_flag.Toggles(provider)


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


class DummyClass:
    def __init__(self, feature_toggles: ioet_feature_flag.Toggles):
        self._toggles = feature_toggles

    @staticmethod
    def _usage(
        get_toggles: typing.Callable,
        when_on,
        when_off,
        context: typing.Optional[ioet_feature_flag.ToggleContext] = None,
    ):
        is_new_greetings_message_enabled = get_toggles(
            ["is_new_greetings_message_enabled"],
            context
        )
        if is_new_greetings_message_enabled:
            return when_on
        return when_off

    def run(self) -> str:
        use_greetings_message = self._toggles.toggle_decision(self._usage)

        cancellation_text = use_greetings_message(
            when_on="Hello",
            when_off="Hi",
        )

        return cancellation_text
