from typing import TYPE_CHECKING
from uuid import uuid4

from datagen.function.commands.command import Command
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.function import Function
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.snbtserializer import SNBTSerializer

if TYPE_CHECKING:
    from datagen.function.commands._data.entitydata import EntityData, BlockEntityData


class RunFunction(Command):
    def __init__(self, func: Function | Identifier | FunctionMacroArgument, args: dict | DataStorage | "EntityData | BlockEntityData" | None = None) -> None:
        super().__init__()
        if isinstance(func, (Identifier)):
            func = Function.of(func)
        elif isinstance(func, FunctionMacroArgument):
            func = func.cast(Function)
        self.func = func
        self.args = args

    def _obfuscated_id(self) -> str:
        if isinstance(self.func, FunctionMacroArgument):
            return str(self.func)
        ns = self.func.id.get_namespace()
        path = self.func.id.get_path()
        return f"{ns}:{Obfuscator.obfuscate_path(ns, path, 'identifiers.functions')}".lower()

    def to_string(self) -> str:
        if self.args is not None:
            if isinstance(self.args, DataStorage):
                return self.auto_macro(f"function {self._obfuscated_id()} with storage {self.args}")
            from datagen.function.commands._data.entitydata import EntityData as ED, BlockEntityData as BED
            if isinstance(self.args, ED):
                _temp_id = f"temp:{uuid4()}"
                return self.auto_macro(
                    f"data modify storage {_temp_id} root set from entity {self.args.get_target()}\n"
                    f"function {self._obfuscated_id()} with storage {_temp_id}"
                )
            if isinstance(self.args, BED):
                _temp_id = f"temp:{uuid4()}"
                return self.auto_macro(
                    f"data modify storage {_temp_id} root set from block {self.args.get_pos()}\n"
                    f"function {self._obfuscated_id()} with storage {_temp_id}"
                )
            args_snbt = SNBTSerializer.serialize(self.args)
            return self.auto_macro(f"function {self._obfuscated_id()} {args_snbt}")
        else:
            return self.auto_macro(f"function {self._obfuscated_id()}")