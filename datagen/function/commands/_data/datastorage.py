from typing import TYPE_CHECKING, TypeAlias

from datagen.function.commands.customcommand import CustomCommand
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

    def __str__(self): return self.id.to_string()
    def to_string(self): return str(self)

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        return CustomCommand(f"data modify storage {self.id} {key} set value {value}")
    
    def set_from_block(self, key: TKey, pos: "BlockPosition", path: str) -> CustomCommand:
        return CustomCommand(f"data modify storage {self.id} {key} set from block {pos} {path}")
    
    def set_from_entity(self, key: TKey, target: TargetSelector, path: str = '') -> CustomCommand:
        return CustomCommand(f"data modify storage {self.id} {key} set from entity {target}{' ' if path else ''}{path}")

    def set_from_score_player(self, key: TKey, player: ScoreboardPlayer) -> CustomCommand:
        return CustomCommand(f"execute store result storage {self.id} {key} int 1 run scoreboard players get {player.name} {player.objective}")

    def get(self, key: TKey, *, scale: float | None = None) -> CustomCommand:
        if scale is not None:
            return CustomCommand(f"data get storage {self.id} {key} {scale}")
        else:
            return CustomCommand(f"data get storage {self.id} {key}")
        
    def merge(self, value: TAny) -> CustomCommand:
        return CustomCommand(f"data merge storage {self.id} {value}")
    
    def remove(self, key: TKey) -> CustomCommand:
        return CustomCommand(f"data remove storage {self.id} {key}")
    
    @staticmethod
    def of(id: Identifier) -> "DataStorage":
        return DataStorage(id)