from typing import TYPE_CHECKING, TypeAlias

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.obfuscator import Obfuscator
if TYPE_CHECKING:
    from datagen.function.function import Function
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.scoreboard.player import ScoreboardPlayer

class DataStorage():
    TKey: TypeAlias = "str | int | float | bool | Identifier | FunctionMacroArgument"
    TAny: TypeAlias = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument"

    def __init__(self, id: Identifier):
        self.id = id

    def __str__(self): return self._id_str()
    def to_string(self): return str(self)

    def _id_str(self) -> str:
        namespace = self.id.get_namespace()
        path = self.id.get_path()
        return f"{namespace}:{Obfuscator.obfuscate_path(namespace, path)}".lower()

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        return CustomCommand(f"data modify storage {self._id_str()} {key} set value {value}")
    
    def set_from_block(self, key: TKey, pos: "BlockPosition", path: str) -> CustomCommand:
        return CustomCommand(f"data modify storage {self._id_str()} {key} set from block {pos} {path}")
    
    def set_from_entity(self, key: TKey, target: TargetSelector, path: str = '') -> CustomCommand:
        return CustomCommand(f"data modify storage {self._id_str()} {key} set from entity {target}{' ' if path else ''}{path}")

    def set_from_score_player(self, key: TKey, player: ScoreboardPlayer) -> CustomCommand:
        return CustomCommand(f"execute store result storage {self._id_str()} {key} int 1 run scoreboard players get {player} {player.objective}")

    def set_from_function_return(self, key: TKey, function: "Identifier | Function") -> CustomCommand:
        from datagen.function.function import Function as Func
        if isinstance(function, Func):
            ns = function.id.get_namespace()
            path = function.id.get_path()
            func_str = f"{ns}:{Obfuscator.obfuscate_path(ns, path)}".lower()
        else:
            ns = function.get_namespace()
            path = function.get_path()
            func_str = f"{ns}:{Obfuscator.obfuscate_path(ns, path)}".lower()
        return CustomCommand(f"execute store result storage {self._id_str()} {key} int 1 run function {func_str}")

    def get(self, key: TKey, *, scale: float | None = None) -> CustomCommand:
        if scale is not None:
            return CustomCommand(f"data get storage {self._id_str()} {key} {scale}")
        else:
            return CustomCommand(f"data get storage {self._id_str()} {key}")
        
    def merge(self, value: TAny) -> CustomCommand:
        return CustomCommand(f"data merge storage {self._id_str()} {value}")
    
    def remove(self, key: TKey) -> CustomCommand:
        return CustomCommand(f"data remove storage {self._id_str()} {key}")
    
    @staticmethod
    def of(id: Identifier) -> "DataStorage":
        return DataStorage(id)