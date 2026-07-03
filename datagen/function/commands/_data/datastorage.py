from typing import TYPE_CHECKING, _TypedDict
from uuid import UUID

from datagen.types.util.reprs import *
from datagen.function.commands.bossbar import BossBar
from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.repr.entityuuid import EntityUUID
if TYPE_CHECKING:
    from datagen.function.commands._data.entitydata import EntityDataValue, BlockEntityDataValue, EntityData, BlockEntityData
    from datagen.function.function import Function
    from datagen.utils.scoreboard.player import ScoreboardPlayer
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector

class DataStorage[D: dict | _TypedDict]():
    type TKey = "str | int | float | bool | Identifier | FunctionMacroArgument"
    type TAny = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument | EntityUUID | EntityDataValue | EntityData | BlockEntityDataValue | BlockEntityData | DataStorageValue | DataStorage"

    def __init__(self, id: Identifier | FunctionMacroArgument | str):
        self.id = id

    def __str__(self): return self._id_str()
    def to_string(self): return str(self)

    def _id_str(self) -> str:
        if isinstance(self.id, (FunctionMacroArgument, str)):
            return str(self.id)
        namespace = self.id.get_namespace()
        path = self.id.get_path()
        return f"{namespace}:{Obfuscator.obfuscate_path(namespace, path, 'identifiers.data_storages')}".lower()

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        from datagen.function.commands._data.entitydata import EntityDataValue as EDV, BlockEntityDataValue as BEDV, EntityData as ED, BlockEntityData as BED
        if isinstance(value, FunctionMacroArgument):
            _v = str(value)
            q = "'" if '"' in _v else '"'
            if q == "'":
                _v = _v.replace("'", "\\'")
            return CustomCommand(f"data modify storage {self._id_str()} {key} set value {q}{_v}{q}")
        if isinstance(value, BaseText):
            value = str(value)
        if isinstance(value, str):
            q = "'" if '"' in value else '"'
            v = value.replace("'", "\\'") if q == "'" else value
            return CustomCommand(f"data modify storage {self._id_str()} {key} set value {q}{v}{q}")
        if isinstance(value, bool):
            return CustomCommand(f'data modify storage {self._id_str()} {key} set value {"true" if value else "false"}')
        if isinstance(value, EntityUUID):
            return CustomCommand(f'data modify storage {self._id_str()} {key} set value "{value.to_string()}"')
        if isinstance(value, DataStorageValue):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from storage {value.storage._id_str()} {value.key}")
        if isinstance(value, EDV):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from entity {value.get_entity().get_target()} {value.get_key()}")
        if isinstance(value, BEDV):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from block {value.get_block_entity().get_pos()} {value.get_key()}")
        if isinstance(value, DataStorage):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from storage {value._id_str()}")
        if isinstance(value, ED):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from entity {value.get_target()}")
        if isinstance(value, BED):
            return CustomCommand(f"data modify storage {self._id_str()} {key} set from block {value.get_pos()}")
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
            func_str = f"{ns}:{Obfuscator.obfuscate_path(ns, path, 'identifiers.functions')}".lower()
        else:
            ns = function.get_namespace()
            path = function.get_path()
            func_str = f"{ns}:{Obfuscator.obfuscate_path(ns, path, 'identifiers.functions')}".lower()
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
    type TAny = "T | FunctionMacroArgument | Identifier | Function | ScoreboardPlayer | DataStorageValue | DataStorage | EntityDataValue | EntityData | BlockEntityDataValue | BlockEntityData | UUID | EntityUUID"  # type: ignore
    def __init__(self, storage: DataStorage, key: DataStorage.TKey):
        self.storage = storage
        self.key = key

    def __getitem__(self, key: int | str | float | bool | Identifier | FunctionMacroArgument) -> "DataStorageValue":
        if isinstance(key, (int)):
            return DataStorageValue(self.storage, f"{self.key}[{key}]")
        return DataStorageValue(self.storage, f'{self.key}.{str(key)}')

    def set(self, value: "DataStorageValue.TAny") -> Command:
        from datagen.function.commands._data.entitydata import EntityData, EntityDataValue, BlockEntityData, BlockEntityDataValue
        from datagen.function.function import Function
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(value, DataStorageValue):
            # /data modify storage ns:name path set from storage ns2:name2 path2
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from storage {value.storage._id_str()} {value.key}")
        elif isinstance(value, EntityDataValue):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from entity {value.get_entity().get_target()} {value.get_key()}")
        elif isinstance(value, BlockEntityDataValue):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from block {value.get_block_entity().get_pos()} {value.get_key()}")
        elif isinstance(value, (Function, Identifier)):
            return self.storage.set_from_function_return(str(self.key), value)
        elif isinstance(value, ScoreboardPlayer):
            return self.storage.set_from_score_player(str(self.key), value)
        elif isinstance(value, FunctionMacroArgument):
            return self.storage.set(str(self.key), value)
        elif isinstance(value, DataStorage):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from storage {value._id_str()}")
        elif isinstance(value, EntityData):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from entity {value.get_target()}")
        elif isinstance(value, BlockEntityData):
            return CustomCommand(f"data modify storage {self.storage._id_str()} {self.key} set from block {value.get_pos()}")
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
        elif isinstance(value, Command):
            cmd = f"execute store result storage {self.storage._id_str()} {self.key} int 1 run {value.raw()}"
            return CustomCommand(['', '$']['$' in cmd] + cmd)
        else:
            return self.storage.set(self.key, value)
    
    def get(self, scale: float | None = None) -> Command:
        return self.storage.get(self.key, scale=scale)
    
    def merge(self, value: dict) -> Command:
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

    def from_score(self, player: "ScoreboardPlayer") -> Command:
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int 1 run scoreboard players get {player} {player.objective}")

    def to_data(self, into: "DataStorageValue | EntityDataValue | BlockEntityDataValue", scale: float = 1) -> Command:
        from datagen.function.commands._data.entitydata import EntityDataValue as EDV, BlockEntityDataValue as BEDV
        if isinstance(into, EDV):
            return CustomCommand(f"execute store result entity {into.get_entity().get_target()} {into.get_key()} int {scale} run data get storage {self.storage._id_str()} {self.key}")
        elif isinstance(into, BEDV):
            return CustomCommand(f"execute store result block {into.get_block_entity().get_pos()} {into.get_key()} int {scale} run data get storage {self.storage._id_str()} {self.key}")
        return CustomCommand(f"execute store result storage {into.storage._id_str()} {into.key} int {scale} run data get storage {self.storage._id_str()} {self.key}")

    def from_data(self, from_: "DataStorageValue | EntityDataValue | BlockEntityDataValue", scale: float = 1) -> Command:
        from datagen.function.commands._data.entitydata import EntityDataValue as EDV, BlockEntityDataValue as BEDV
        if isinstance(from_, EDV):
            return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int {scale} run data get entity {from_.get_entity().get_target()} {from_.get_key()}")
        elif isinstance(from_, BEDV):
            return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int {scale} run data get block {from_.get_block_entity().get_pos()} {from_.get_key()}")
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int {scale} run data get storage {from_.storage._id_str()} {from_.key}")

    def to_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{Obfuscator.obfuscate_path(id.get_namespace(), id.get_path())}".lower()
        return CustomCommand(f"execute store result bossbar {_id} value int 1 run data get storage {self.storage._id_str()} {self.key}")
    
    def from_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{Obfuscator.obfuscate_path(id.get_namespace(), id.get_path())}".lower()
        return CustomCommand(f"execute store result storage {self.storage._id_str()} {self.key} int 1 run bossbar get {_id} value")
    
    def set_into(self, into: "DataStorageValue | EntityDataValue | BlockEntityDataValue") -> Command:
        from datagen.function.commands._data.entitydata import EntityDataValue as EDV, BlockEntityDataValue as BEDV
        if isinstance(into, EDV):
            return CustomCommand(f"data modify entity {into.get_entity().get_target()} {into.get_key()} set from storage {self.storage._id_str()} {self.key}")
        elif isinstance(into, BEDV):
            return CustomCommand(f"data modify block {into.get_block_entity().get_pos()} {into.get_key()} set from storage {self.storage._id_str()} {self.key}")
        return CustomCommand(f"data modify storage {into.storage._id_str()} {into.key} set from storage {self.storage._id_str()} {self.key}")

    def __lshift__(self, other: "TAny | DataStorage | EntityData | BlockEntityData") -> Command:
        from datagen.function.commands._data.entitydata import EntityDataValue as EDV, BlockEntityDataValue as BEDV, EntityData as ED, BlockEntityData as BED
        if isinstance(other, (DataStorageValue, EDV, BEDV)):
            return self.set_into(other)  # type: ignore
        elif isinstance(other, (DataStorage, ED, BED)):
            return self.set(other)
        else:
            return self.set(other)