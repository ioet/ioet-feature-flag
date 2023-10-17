import dummy_module


def test_get_name():
    assert dummy_module.get_name() == "name-a"


def test_get_name_user():
    assert dummy_module.get_name_user() == "name-a"
