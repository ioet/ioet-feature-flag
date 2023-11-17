import pytest


from ioet_feature_flag.helpers.validators import (
    are_args_boolean,
    are_args_different_types,
    are_args_invalid_functions,
)


def _dummy_function_a(_dummy_arg):
    return True


def _dummy_function_b() -> str:
    return False


def _dummy_valid_function_a() -> str:
    return "123"


def _dummy_valid_function_b():
    pass


def _dummy_valid_function_c():
    print('test')
    return True


@pytest.mark.parametrize(
    "args, expected_result",
    [
        ([True], True),
        ([False, True], True),
        ([123, True], True),
        ([123], False),
        ([123, "123"], False),
        ([], False),
    ],
)
def test_are_args_boolean(args, expected_result):
    assert are_args_boolean(*args) == expected_result


@pytest.mark.parametrize(
    "args, expected_result",
    [
        ([], False),
        ([True], False),
        ([False, True], False),
        ([123, True], True),
        ([123, "123"], True),
        ([123, 123], False),
        (["123", "123"], False),
        ([123, 456, "123"], True),
        ([123, "123", 456], True),
        (["123", 123, 456], True),
    ],
)
def test_are_args_different_types(args, expected_result):
    assert are_args_different_types(*args) == expected_result


@pytest.mark.parametrize(
    "args, expected_result",
    [
        ([], False),
        ([True, lambda: True], False),
        ([lambda: True], True),
        ([lambda: False], True),
        ([_dummy_function_a], True),
        ([_dummy_function_b], True),
        ([_dummy_valid_function_a], False),
        ([_dummy_valid_function_b], False),
        ([_dummy_valid_function_c], False),
        ([123], False),
        (["123"], False),
        ([Exception()], False),
        ([{}], False),
        ([[]], False),
    ],
)
def test_are_args_invalid_functions(args, expected_result):
    assert are_args_invalid_functions(*args) == expected_result
