from typing import TYPE_CHECKING

from datagen.function.commands.command import Command
if TYPE_CHECKING:
    from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class CommandArray():
    _last = None
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
        from datagen.function.function import Function
        if isinstance(other, CommandArray):
            self.commands.extend(other.commands)
        elif isinstance(other, Function):
            self.commands.extend(other.run())
        else:
            self.commands.append(other)
        return self

    def __enter__(self):
        from datagen.function.function import Function
        CommandArray._last = Function.current_function
        Function.current_function = self # type: ignore
        
        self.__previous_array = CommandArray.__current_array
        CommandArray.__current_array = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from datagen.function.function import Function
        Function.current_function = CommandArray._last
        CommandArray.__current_array = self.__previous_array

    def to_function(self, id: Identifier | None = None) -> "Function":
        from datagen.function.function import Function
        with ~ Function(id) as _:
            ~ self
        return _