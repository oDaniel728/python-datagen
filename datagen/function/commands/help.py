from typing import overload

from datagen.function.commands.customcommand import CustomCommand


class Help(CustomCommand):

    @overload
    def __init__(self, command: str) -> None: ...
    @overload
    def __init__(self) -> None: ...

    def __init__(self, command: str | None = None) -> None:
        if command is not None:
            super().__init__(f"help {command}")
        else:
            super().__init__("help")