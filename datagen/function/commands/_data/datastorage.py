from typing import TYPE_CHECKING, TypeAlias

from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.scoreboard.objective import ScoreboardObjective
if TYPE_CHECKING:
    from datagen.function.function import Function
    from datagen.utils.scoreboard.player import ScoreboardPlayer
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector

class DataStorage():
    type TKey = "str | int | float | bool | Identifier | FunctionMacroArgument"
    type TAny = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument"

    def __init__(self, id: Identifier):
        self.id = id

    def __str__(self): return self._id_str()
    def to_string(self): return str(self)

    def _id_str(self) -> str:
        namespace = self.id.get_namespace()
        path = self.id.get_path()
        return f"{namespace}:{Obfuscator.obfuscate_path(namespace, path)}".lower()

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        if isinstance(value, FunctionMacroArgument):
            return CustomCommand(f'data modify storage {self._id_str()} {key} set value "{value}"')
        if isinstance(value, str):
            return CustomCommand(f'data modify storage {self._id_str()} {key} set value "{value}"')
        return CustomCommand(f"data modify storage {self._id_str()} {key} set value {value}")
    
    def set_from_block(self, key: TKey, pos: "BlockPosition", path: str) -> CustomCommand:
        return CustomCommand(f"data modify storage {self._id_str()} {key} set from block {pos} {path}")
    
    def set_from_entity(self, key: TKey, target: TargetSelector, path: str = '') -> CustomCommand:
        return CustomCommand(f"data modify storage {self._id_str()} {key} set from entity {target}{' ' if path else ''}{path}")

    def set_from_score_player(self, key: TKey, player: "ScoreboardPlayer") -> CustomCommand:
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

    def rset(self, d: dict[str, TAny | ScoreboardPlayer | (Function | Identifier)]) -> CommandArray:
        cmds = CommandArray([])
        for k, v in d.items():
            if isinstance(v, ScoreboardPlayer):
                cmds += self.set_from_score_player(k, v)
            elif isinstance(v, (Function, Identifier)):
                cmds += self.set_from_function_return(k, v)
            else:
                cmds += self.set(k, v)
        return cmds

    def __getitem__(self, key: TKey) -> DataStorageValue:
        return DataStorageValue(self, key)

    def __setitem__(self, key: TKey, value: "DataStorageValue.TAny"):
        return self[key].set(value)

class DataStorageValue[T: DataStorage.TAny]():
    type TAny = "T | FunctionMacroArgument | Identifier | Function | ScoreboardPlayer | DataStorageValue"
    def __init__(self, storage: DataStorage, key: DataStorage.TKey):
        self.storage = storage
        self.key = key

    def set(self, value: "DataStorageValue.TAny") -> Command:
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(value, DataStorageValue):
            from datagen.function.commands.execute import Execute
            # /execute store result storage ns:id path int 1 run data get storage ns2:id2 path2 1
            return Execute().STORE("result", "storage", self.storage, str(self.key), "int", 1).RUN(value.get(scale=1))
        elif isinstance(value, (Function, Identifier)):
            return self.storage.set_from_function_return(str(self.key), value)
        elif isinstance(value, ScoreboardPlayer):
            return self.storage.set_from_score_player(str(self.key), value)
        elif isinstance(value, FunctionMacroArgument):
            return self.storage.set(str(self.key), value)
        else:
            return self.storage.set(self.key, value)
    
    def get(self, scale: float | None = None) -> CustomCommand:
        return self.storage.get(self.key, scale=scale)
    
    def merge(self, value: dict) -> CustomCommand:
        return self.storage.merge(value)
    
    def remove(self) -> CustomCommand:
        return self.storage.remove(self.key)

    def to_score(self, set: bool = False) -> "ScoreboardPlayer":
        from datagen.function.commands.execute import Execute
        plr = (~ ScoreboardObjective.TEMP)["__" + self.storage._id_str() + "." + str(self.key)]
        if set:
            ~ (
                Execute()
                .STORE("result", "storage", self.storage, str(self.key), "int", 1)
                .RUN(self.get())
            )
        return plr

    def from_score(self, player: "ScoreboardPlayer") -> CustomCommand:
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int 1 run scoreboard players get {player} {player.objective}")