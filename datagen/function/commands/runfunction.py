from datagen.function.commands.command import Command
from datagen.function.function import Function


class RunFunction(Command):
    def __init__(self, func: Function) -> None:
        self.func = func

    def to_string(self) -> str:
        return self.auto_macro(f"function {self.func.id}") # function namespace:path/to/function