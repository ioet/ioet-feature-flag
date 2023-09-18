import typing


class ToggleContext:
    def __init__(
        self, username: str, role: str, **attributes: typing.Dict[str, typing.Any]
    ) -> None:
        self.username = username
        self.role = role
        self.__dict__ = {**self.__dict__, **attributes}

    def get(self, attribute: str) -> typing.Optional[typing.Any]:
        return self.__dict__.get(attribute, None)
