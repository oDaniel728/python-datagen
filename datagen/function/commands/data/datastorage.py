from typing import TYPE_CHECKING, TypeAlias

from datagen.function.commands.customcommand import CustomCommand
if TYPE_CHECKING:
    from datagen.function.commands.data.datafunctionargument import DataFunctionArgument
from datagen.utils.minecraft.identifier import Identifier

class DataStorage():
    TKey: TypeAlias = "str | int | float | bool | Identifier"
    TAny: TypeAlias = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None"


    def __init__(self, id: Identifier, initial_value: TAny = {}):
        self.id = id

    def __str__(self): return self.id.to_string()
    def to_string(self): return str(self)

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        return CustomCommand(f"data modify storage {self.id} {key} set value {value}")
    
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
    def of(id: Identifier, initial_value: TAny = {}) -> "DataStorage":
        return DataStorage(id, initial_value)
    
    @staticmethod
    def args(values: list[TAny]) -> "DataFunctionArgument":
        from datagen.function.commands.data.datafunctionargument import DataFunctionArgument
        return DataFunctionArgument(values)