import dummy_module

import ioet_feature_flag


def test_get_name():
    assert dummy_module.get_name() == "name-a"


def test_get_name_b():
    assert dummy_module.get_name_b() == "name-b"


def test_get_name_user():
    assert dummy_module.get_name_user() == "name-a"


def test_object_oriented():
    provider = ioet_feature_flag.YamlToggleProvider(
        './feature_toggles/feature-toggles.yaml'
    )
    toggles = ioet_feature_flag.Toggles(provider)
    dummy_object = dummy_module.DummyClass(toggles)
    assert dummy_object.run() == "Hello"
