import ioet_feature_flag

toggles = ioet_feature_flag.Toggles()


@toggles.toggle_decision
def dummy_decision(get_toggles, when_on, when_off):
    is_enabled = get_toggles(["dummy-flag"])
    if is_enabled:
        return when_on
    return when_off


def get_name():
    return dummy_decision(
        when_on="name-a",
        when_off="name-b",
    )
