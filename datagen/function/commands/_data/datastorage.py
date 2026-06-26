from typing import TYPE_CHECKING, _TypedDict, TypeAlias, TypedDict
from uuid import UUID

from datagen.types.util.reprs import *
from datagen.function.commands.bossbar import BossBar
from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.repr.entityuuid import EntityUUID
if TYPE_CHECKING:
    from datagen.function.function import Function
    from datagen.utils.scoreboard.player import ScoreboardPlayer
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector

class DataStorage[D: dict | _TypedDict]():
    type TKey = "str | int | float | bool | Identifier | FunctionMacroArgument"
    type TAny = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument"

    def __init__(self, id: Identifier | FunctionMacroArgument | str):
        self.id = id

    def __str__(self): return self._id_str()
    def to_string(self): return str(self)

    def _id_str(self) -> str:
        if isinstance(self.id, (FunctionMacroArgument, str)):
            return str(self.id)
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

    def rset(self, d: dict[str, "DataStorageValue.TAny"]) -> CommandArray:
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        cmds = CommandArray([])
        for k, v in d.items():
            cmds += self[k].set(v)
        return cmds

    def __getitem__(self, key: TKey) -> DataStorageValue:
        return DataStorageValue(self, key)

    def __setitem__(self, key: TKey, value: "DataStorageValue.TAny"):
        return self[key].set(value)

class DataStorageValue[T]():
    type TAny = "T | FunctionMacroArgument | Identifier | Function | ScoreboardPlayer | DataStorageValue | DataStorage | UUID | EntityUUID"
    def __init__(self, storage: DataStorage, key: DataStorage.TKey):
        self.storage = storage
        self.key = key

    def __getitem__(self, key: int | str | float | bool | Identifier | FunctionMacroArgument) -> "DataStorageValue":
        if isinstance(key, (int)):
            return DataStorageValue(self.storage, f"{self.key}[{key}]")
        return DataStorageValue(self.storage, f'{self.key}.{str(key)}')

    def set(self, value: "DataStorageValue.TAny") -> Command:
        from datagen.function.function import Function
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(value, DataStorageValue):
            # from datagen.function.commands.execute import Execute
            # # /execute store result storage ns:id path int 1 run data get storage ns2:id2 path2 1
            # return Execute().STORE("result", "storage", self.storage, str(self.key), "int", 1).RUN(value.get(scale=1))
            # /data modify storage ns:name path set from storage ns2:name2 path2
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from storage {value.storage._id_str()} {value.key}")
        elif isinstance(value, (Function, Identifier)):
            return self.storage.set_from_function_return(str(self.key), value)
        elif isinstance(value, ScoreboardPlayer):
            return self.storage.set_from_score_player(str(self.key), value)
        elif isinstance(value, FunctionMacroArgument):
            return self.storage.set(str(self.key), value)
        elif isinstance(value, DataStorage):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from storage {value._id_str()}")
        elif isinstance(value, UUID):
            # [I; ...]
            _values: tuple4[int] = (
                value.int >> 96 & 0xFFFFFFFF, 
                value.int >> 64 & 0xFFFFFFFF, 
                value.int >> 32 & 0xFFFFFFFF, 
                value.int & 0xFFFFFFFF
            )
            return self.storage.set(str(self.key), f"[I; {_values[0]}, {_values[1]}, {_values[2]}, {_values[3]}]")
        elif isinstance(value, EntityUUID):
            return self.storage.set(str(self.key), value.to_string())
        else:
            return self.storage.set(self.key, value)
    
    def get(self, scale: float | None = None) -> CustomCommand:
        return self.storage.get(self.key, scale=scale)
    
    def merge(self, value: dict) -> CustomCommand:
        return self.storage.merge(value)
    
    def remove(self) -> CustomCommand:
        return self.storage.remove(self.key)

    def to_score(self, set: bool = False):
        from datagen.function.commands.execute import Execute
        from datagen.utils.scoreboard.objective import ScoreboardObjective
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

    def to_data(self, into: "DataStorageValue",  scale: float = 1) -> CustomCommand:
        return CustomCommand(f"execute store result storage {into.storage._id_str()} {into.key} int {scale} run data get storage {self.storage._id_str()} {self.key}")

    def from_data(self, from_: "DataStorageValue", scale: float = 1) -> CustomCommand:
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int {scale} run data get storage {from_.storage._id_str()} {from_.key}")

    def to_bossbar(self, bossbar: "Identifier | BossBar") -> CustomCommand:
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{Obfuscator.obfuscate_path(id.get_namespace(), id.get_path())}".lower()
        return CustomCommand(f"execute store result bossbar {_id} value int 1 run data get storage {self.storage._id_str()} {self.key}")
    
    def from_bossbar(self, bossbar: "Identifier | BossBar") -> CustomCommand:
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{Obfuscator.obfuscate_path(id.get_namespace(), id.get_path())}".lower()
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int 1 run bossbar get {_id} value")
    