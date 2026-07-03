from typing import TYPE_CHECKING

from datagen.function.commands.command import Command
if TYPE_CHECKING:
    from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class CommandArray():
    __current_array: CommandArray | None = None
    @staticmethod
    def get_current_array() -> CommandArray | None:
        return CommandArray.__current_array
    
    def __init__(self, commands: list[Command]):
        self.commands = commands

    def __iter__(self):
        return iter(self.commands)

    def __invert__(self):
        for _ in self:
            ~ _

    def __iadd__(self, other: Command | CommandArray | Function):
        if isinstance(other, CommandArray):
            self.commands.extend(other.commands)
        elif isinstance(other, Function):
            self += other.run()
        else:
            self.commands.append(other)
        return self

    def __enter__(self):
        self.__previous_array = CommandArray.__current_array
        CommandArray.__current_array = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        CommandArray.__current_array = self.__previous_array

    def to_function(self, id: Identifier | None = None) -> "Function":
        from datagen.function.function import Function
        from datagen.function.anonymousfunction import AnonymousFunction
        if id is None:
            with AnonymousFunction() as _:
                ~ self
            return _
        else:
            with Function(id) as _:
                ~ self
            return _