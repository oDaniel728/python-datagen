from datagen.function.commands.command import Command
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class RunFunction(Command):
    def __init__(self, func: Function | Identifier) -> None:
        super().__init__()
        self.func = func if isinstance(func, Function) else Function.of(func)

    def to_string(self) -> str:
        return self.auto_macro(f"function {self.func.id}") # function namespace:path/to/function