from datagen.function.commands.command import Command


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

    def __iadd__(self, other: Command | CommandArray):
        if isinstance(other, CommandArray):
            self.commands.extend(other.commands)
        else:
            self.commands.append(other)
        return self

    def __enter__(self):
        self.__previous_array = CommandArray.__current_array
        CommandArray.__current_array = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        CommandArray.__current_array = self.__previous_array