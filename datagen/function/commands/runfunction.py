from datagen.function.commands.command import Command
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.snbtserializer import SNBTSerializer


class RunFunction(Command):
    def __init__(self, func: Function | Identifier, args: dict | DataStorage | None = None) -> None:
        super().__init__()
        self.func = func if isinstance(func, Function) else Function.of(func)
        self.args = args

    def to_string(self) -> str:
        if self.args is not None:
            if isinstance(self.args, DataStorage):
                return self.auto_macro(f"function {self.func.id} with storage {self.args.id}")
            else:
                args_snbt = SNBTSerializer.serialize(self.args)
                return self.auto_macro(f"function {self.func.id} {args_snbt}")
        else:
            return self.auto_macro(f"function {self.func.id}") # function namespace:path/to/function