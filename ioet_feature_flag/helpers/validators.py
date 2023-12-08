
_INVALID_FUNCTION_CODES = [
    (lambda: True).__code__.co_code,
    (lambda: False).__code__.co_code,
]


def are_args_boolean(*args) -> bool:
    for arg in args:
        if isinstance(arg, bool):
            return True
    return False


def are_args_different_types(*args) -> bool:
    if not args:
        return False
    types_set = set(
        str(type(arg)) for arg in args
    )
    return len(types_set) > 1


def are_args_invalid_functions(*args) -> bool:
    if not all(hasattr(arg, '__code__') for arg in args):
        return False

    for arg in args:
        if (
            arg.__code__.co_code in _INVALID_FUNCTION_CODES
            and isinstance(arg(*[1 for _ in range(arg.__code__.co_argcount)]), bool)
        ):
            return True

    return False
