from datagen.function.commands.command import Command
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class RunFunction(Command):
    def __init__(self, func: Function | Identifier, args: DataStorage | None = None) -> None:
        super().__init__()
        self.func = func if isinstance(func, Function) else Function.of(func)
        self.args = args

    def to_string(self) -> str:
        if self.args is not None:
            return self.auto_macro(f"function {self.func.id} with storage {self.args.id}")
        else:
            return self.auto_macro(f"function {self.func.id}") # function namespace:path/to/function