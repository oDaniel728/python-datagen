from typing import TYPE_CHECKING, _TypedDict
from uuid import UUID

from datagen.function.commands.bossbar import BossBar
from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands._data.datastorage import DataStorage, DataStorageValue
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.repr.entityuuid import EntityUUID

if TYPE_CHECKING:
    from datagen.function.function import Function
    from datagen.utils.scoreboard.player import ScoreboardPlayer

from datagen.function.functionmacroargument import FunctionMacroArgument


class EntityData[_TEntity: (TargetSelector, str)]():
    """Wrapper for Minecraft /data entity commands.

    Allows reading, modifying, and removing NBT data from entities
    using a chained key interface similar to DataStorage.

    Examples:

        >>> target = TargetSelector.SELF
        >>> ed = EntityData(target)
        >>> ed["Health"].set(20.0)
        >>> ed["CustomName"].get()
        >>> ed["Inventory[0]"].remove()
    """

    type TKey = "str | int | float | bool | Identifier | FunctionMacroArgument"
    type TAny = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument | EntityUUID"

    def __init__(self, target: TargetSelector | str) -> None:
        """Inicializa EntityData com um seletor de entidade.

        Args:
            target: seletor de entidade (ex: @s, @p, @e[...])

        Examples:

            >>> ed = EntityData(TargetSelector.SELF)
        """
        self.__target = target

    def __str__(self) -> str:
        return str(self.__target)

    def to_string(self) -> str:
        """Retorna a representação em string do target."""
        return str(self)

    def get_target(self) -> TargetSelector | str:
        """Retorna o seletor de entidade."""
        return self.__target

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        """Define um valor NBT na entidade.

        Args:
            key: caminho NBT
            value: valor a ser definido

        Returns:
            CustomCommand com data modify entity ... set value ...

        Examples:

            >>> ed.set("Health", 20.0)
        """
        if isinstance(value, FunctionMacroArgument):
            _v = str(value)
            q = "'" if '"' in _v else '"'
            if q == "'":
                _v = _v.replace("'", "\\'")
            return CustomCommand(f"data modify entity {self.__target} {key} set value {q}{_v}{q}")
        if isinstance(value, BaseText):
            value = str(value)
        if isinstance(value, str):
            q = "'" if '"' in value else '"'
            v = value.replace("'", "\\'") if q == "'" else value
            return CustomCommand(f"data modify entity {self.__target} {key} set value {q}{v}{q}")
        if isinstance(value, bool):
            return CustomCommand(f'data modify entity {self.__target} {key} set value {"true" if value else "false"}')
        if isinstance(value, EntityUUID):
            return CustomCommand(f'data modify entity {self.__target} {key} set value "{value.to_string()}"')
        return CustomCommand(f"data modify entity {self.__target} {key} set value {value}")

    def set_from_block(self, key: TKey, pos: BlockPosition, path: str) -> CustomCommand:
        """Copia dados de um block entity para a entidade.

        Args:
            key: caminho NBT de destino na entidade
            pos: posição do bloco
            path: caminho NBT de origem no bloco

        Examples:

            >>> ed.set_from_block("TileData", BlockPosition(0, 5, 0), "")
        """
        return CustomCommand(f"data modify entity {self.__target} {key} set from block {pos} {path}")

    def set_from_entity(self, key: TKey, target: TargetSelector, path: str = "") -> CustomCommand:
        """Copia dados de outra entidade para esta.

        Args:
            key: caminho NBT de destino
            target: seletor da entidade de origem
            path: caminho NBT de origem

        Examples:

            >>> ed.set_from_entity("Health", TargetSelector("@e", {"type": "minecraft:zombie", "limit": 1}))
        """
        return CustomCommand(f"data modify entity {self.__target} {key} set from entity {target}{' ' if path else ''}{path}")

    def set_from_storage(self, key: TKey, storage: DataStorage, path: str = "") -> CustomCommand:
        """Copia dados de um storage para a entidade.

        Args:
            key: caminho NBT de destino
            storage: storage de origem
            path: caminho NBT de origem no storage
        """
        return CustomCommand(f"data modify entity {self.__target} {key} set from storage {storage._id_str()} {path}")

    def set_from_score_player(self, key: TKey, player: "ScoreboardPlayer") -> CustomCommand:
        """Define um valor na entidade a partir de um scoreboard player.

        Args:
            key: caminho NBT de destino
            player: jogador do scoreboard

        Examples:

            >>> ed.set_from_score_player("Health", some_player)
        """
        return CustomCommand(f"execute store result entity {self.__target} {key} int 1 run scoreboard players get {player} {player.objective}")

    def set_from_function_return(self, key: TKey, function: "Identifier | Function") -> CustomCommand:
        """Define um valor na entidade a partir do returno de uma função.

        Args:
            key: caminho NBT de destino
            function: função a ser executada

        Examples:

            >>> ed.set_from_function_return("CustomScore", my_function)
        """
        from datagen.function.function import Function as Func
        if isinstance(function, Func):
            ns = function.id.get_namespace()
            path = function.id.get_path()
            func_str = f"{ns}:{path}".lower()
        else:
            ns = function.get_namespace()
            path = function.get_path()
            func_str = f"{ns}:{path}".lower()
        return CustomCommand(f"execute store result entity {self.__target} {key} int 1 run function {func_str}")

    def get(self, key: TKey, *, scale: float | None = None) -> CustomCommand:
        """Obtém um valor NBT da entidade.

        Args:
            key: caminho NBT
            scale: fator de escala opcional

        Examples:

            >>> ed.get("Health")
            >>> ed.get("Health", scale=0.5)
        """
        if scale is not None:
            return CustomCommand(f"data get entity {self.__target} {key} {scale}")
        return CustomCommand(f"data get entity {self.__target} {key}")

    def merge(self, value: TAny) -> CustomCommand:
        """Faz merge de dados NBT na entidade.

        Args:
            value: dict ou SNBT a ser mesclado

        Examples:

            >>> ed.merge({"Health": 20.0, "CustomName": '{"text":"Test"}'})
        """
        return CustomCommand(f"data merge entity {self.__target} {value}")

    def remove(self, key: TKey) -> CustomCommand:
        """Remove um caminho NBT da entidade.

        Args:
            key: caminho NBT a remover

        Examples:

            >>> ed.remove("CustomName")
        """
        return CustomCommand(f"data remove entity {self.__target} {key}")

    def rset(self, d: dict[str, "DataStorageValue.TAny"]) -> CommandArray:
        """Define múltiplos valores de uma vez.

        Args:
            d: dicionário {chave: valor}

        Examples:

            >>> ed.rset({"Health": 20.0, "Air": 300})
        """
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        cmds = CommandArray([])
        for k, v in d.items():
            cmds += self[k].set(v)
        return cmds

    def __getitem__(self, key: TKey) -> "EntityDataValue":
        """Acessa um caminho NBT com suporte a chaining.

        Examples:

            >>> ed["Health"].set(20.0)
            >>> ed["Inventory[0]"].get()
        """
        return EntityDataValue(self, key)

    def __setitem__(self, key: TKey, value: "DataStorageValue.TAny") -> None:
        """Define um valor via atribuição direta.

        Examples:

            >>> ed["Health"] = 20.0
        """
        self[key].set(value)

    @staticmethod
    def of(target: TargetSelector) -> "EntityData":
        """Factory method.

        Args:
            target: seletor de entidade

        Examples:

            >>> EntityData.of(TargetSelector.SELF)
        """
        return EntityData(target)


class BlockEntityData[_TPos: (BlockPosition, str)]():
    """Wrapper for Minecraft /data block commands.

    Allows reading, modifying, and removing NBT data from block entities
    using a chained key interface similar to DataStorage.

    Examples:

        >>> pos = BlockPosition(0, 5, 0)
        >>> bed = BlockEntityData(pos)
        >>> bed["Items"].merge({...})
        >>> bed["CustomName"].get()
    """

    type TKey = "str | int | float | bool | Identifier | FunctionMacroArgument"
    type TAny = "str | int | float | bool | Identifier | list[TAny] | dict[TKey, TAny] | None | FunctionMacroArgument | EntityUUID"

    def __init__(self, pos: BlockPosition) -> None:
        """Inicializa BlockEntityData com uma posição de bloco.

        Args:
            pos: posição do bloco

        Examples:

            >>> bed = BlockEntityData(BlockPosition(10, 64, 10))
        """
        self.__pos = pos

    def __str__(self) -> str:
        return str(self.__pos)

    def to_string(self) -> str:
        """Retorna a representação em string da posição."""
        return str(self)

    def get_pos(self) -> BlockPosition:
        """Retorna a posição do bloco."""
        return self.__pos

    def set(self, key: TKey, value: TAny) -> CustomCommand:
        """Define um valor NBT no block entity.

        Args:
            key: caminho NBT
            value: valor a ser definido

        Examples:

            >>> bed.set("CustomName", '{"text":"Chest"}')
        """
        if isinstance(value, FunctionMacroArgument):
            _v = str(value)
            q = "'" if '"' in _v else '"'
            if q == "'":
                _v = _v.replace("'", "\\'")
            return CustomCommand(f"data modify block {self.__pos} {key} set value {q}{_v}{q}")
        if isinstance(value, BaseText):
            value = str(value)
        if isinstance(value, str):
            q = "'" if '"' in value else '"'
            v = value.replace("'", "\\'") if q == "'" else value
            return CustomCommand(f"data modify block {self.__pos} {key} set value {q}{v}{q}")
        if isinstance(value, bool):
            return CustomCommand(f'data modify block {self.__pos} {key} set value {"true" if value else "false"}')
        if isinstance(value, EntityUUID):
            return CustomCommand(f'data modify block {self.__pos} {key} set value "{value.to_string()}"')
        return CustomCommand(f"data modify block {self.__pos} {key} set value {value}")

    def set_from_block(self, key: TKey, pos: BlockPosition, path: str) -> CustomCommand:
        """Copia dados de outro block entity para este.

        Args:
            key: caminho NBT de destino
            pos: posição do bloco de origem
            path: caminho NBT de origem
        """
        return CustomCommand(f"data modify block {self.__pos} {key} set from block {pos} {path}")

    def set_from_entity(self, key: TKey, target: TargetSelector, path: str = "") -> CustomCommand:
        """Copia dados de uma entidade para o block entity.

        Args:
            key: caminho NBT de destino
            target: seletor da entidade de origem
            path: caminho NBT de origem
        """
        return CustomCommand(f"data modify block {self.__pos} {key} set from entity {target}{' ' if path else ''}{path}")

    def set_from_storage(self, key: TKey, storage: DataStorage, path: str = "") -> CustomCommand:
        """Copia dados de um storage para o block entity.

        Args:
            key: caminho NBT de destino
            storage: storage de origem
            path: caminho NBT de origem no storage
        """
        return CustomCommand(f"data modify block {self.__pos} {key} set from storage {storage._id_str()} {path}")

    def set_from_score_player(self, key: TKey, player: "ScoreboardPlayer") -> CustomCommand:
        """Define um valor no block entity a partir de um scoreboard player.

        Args:
            key: caminho NBT de destino
            player: jogador do scoreboard
        """
        return CustomCommand(f"execute store result block {self.__pos} {key} int 1 run scoreboard players get {player} {player.objective}")

    def set_from_function_return(self, key: TKey, function: "Identifier | Function") -> CustomCommand:
        """Define um valor no block entity a partir do retorno de uma função.

        Args:
            key: caminho NBT de destino
            function: função a ser executada
        """
        from datagen.function.function import Function as Func
        if isinstance(function, Func):
            ns = function.id.get_namespace()
            path = function.id.get_path()
            func_str = f"{ns}:{path}".lower()
        else:
            ns = function.get_namespace()
            path = function.get_path()
            func_str = f"{ns}:{path}".lower()
        return CustomCommand(f"execute store result block {self.__pos} {key} int 1 run function {func_str}")

    def get(self, key: TKey, *, scale: float | None = None) -> CustomCommand:
        """Obtém um valor NBT do block entity.

        Args:
            key: caminho NBT
            scale: fator de escala opcional
        """
        if scale is not None:
            return CustomCommand(f"data get block {self.__pos} {key} {scale}")
        return CustomCommand(f"data get block {self.__pos} {key}")

    def merge(self, value: TAny) -> CustomCommand:
        """Faz merge de dados NBT no block entity.

        Args:
            value: dict ou SNBT a ser mesclado
        """
        return CustomCommand(f"data merge block {self.__pos} {value}")

    def remove(self, key: TKey) -> CustomCommand:
        """Remove um caminho NBT do block entity.

        Args:
            key: caminho NBT a remover
        """
        return CustomCommand(f"data remove block {self.__pos} {key}")

    def rset(self, d: dict[str, "DataStorageValue.TAny"]) -> CommandArray:
        """Define múltiplos valores de uma vez.

        Args:
            d: dicionário {chave: valor}
        """
        cmds = CommandArray([])
        for k, v in d.items():
            cmds += self[k].set(v)
        return cmds

    def __getitem__(self, key: TKey) -> "BlockEntityDataValue":
        """Acessa um caminho NBT com suporte a chaining."""
        return BlockEntityDataValue(self, key)

    def __setitem__(self, key: TKey, value: "DataStorageValue.TAny") -> None:
        """Define um valor via atribuição direta."""
        self[key].set(value)

    @staticmethod
    def of(pos: BlockPosition) -> "BlockEntityData":
        """Factory method.

        Args:
            pos: posição do bloco
        """
        return BlockEntityData(pos)


class EntityDataValue[T]():
    """Valor encadeado de EntityData.

    Permite operações em um caminho NBT específico de uma entidade,
    similar a DataStorageValue.

    Examples:

        >>> ed = EntityData(TargetSelector.SELF)
        >>> ed["Health"].set(20.0)
        >>> ed["Health"].get()
        >>> ed["Inventory[0]"].remove()
    """

    type TAny = "T | FunctionMacroArgument | Identifier | Function | ScoreboardPlayer | EntityDataValue | EntityData | DataStorageValue | DataStorage | UUID | EntityUUID"  # type: ignore

    def __init__(self, entity: EntityData, key: EntityData.TKey) -> None:
        """Inicializa EntityDataValue.

        Args:
            entity: EntityData de origem
            key: caminho NBT
        """
        self.__entity = entity
        self.__key = key

    def get_entity(self) -> EntityData:
        """Retorna o EntityData de origem."""
        return self.__entity

    def get_key(self) -> EntityData.TKey:
        """Retorna a chave/caminho NBT."""
        return self.__key

    def __getitem__(self, key: int | str | float | bool | Identifier | FunctionMacroArgument) -> "EntityDataValue":
        """Acessa sub-caminho (suporta índices numéricos e chaves aninhadas).

        Examples:

            >>> ed["Inventory"][0]
        """
        if isinstance(key, int):
            return EntityDataValue(self.__entity, f"{self.__key}[{key}]")
        return EntityDataValue(self.__entity, f"{self.__key}.{str(key)}")

    def set(self, value: "EntityDataValue.TAny") -> Command:
        """Define o valor no caminho NBT.

        Suporta diversos tipos: valores primitivos, outros EntityDataValue,
        DataStorage, Function, ScoreboardPlayer, UUID, Command.

        Args:
            value: valor a ser definido

        Examples:

            >>> ed["Health"].set(20.0)
            >>> ed["Pos"].set(pos_data_value)
        """
        from datagen.function.function import Function
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(value, EntityDataValue):
            # data modify entity <target> <key> set from entity <other_target> <other_key>
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from entity {value.get_entity().get_target()} {value.get_key()}"
            )
        elif isinstance(value, BlockEntityDataValue):
            # data modify entity <target> <key> set from block <pos> <other_key>
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from block {value.get_block_entity().get_pos()} {value.get_key()}"
            )
        elif isinstance(value, DataStorageValue):
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from storage {value.storage._id_str()} {value.key}"
            )
        elif isinstance(value, (Function, Identifier)):
            return self.__entity.set_from_function_return(self.__key, value)
        elif isinstance(value, ScoreboardPlayer):
            return self.__entity.set_from_score_player(self.__key, value)
        elif isinstance(value, FunctionMacroArgument):
            return self.__entity.set(self.__key, value)
        elif isinstance(value, EntityData):
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from entity {value.get_target()}"
            )
        elif isinstance(value, BlockEntityData):
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from block {value.get_pos()}"
            )
        elif isinstance(value, DataStorage):
            return CustomCommand(
                f"data modify entity {self.__entity.get_target()} {self.__key} "
                f"set from storage {value._id_str()}"
            )
        elif isinstance(value, UUID):
            _values: tuple[int, int, int, int] = (
                value.int >> 96 & 0xFFFFFFFF,
                value.int >> 64 & 0xFFFFFFFF,
                value.int >> 32 & 0xFFFFFFFF,
                value.int & 0xFFFFFFFF,
            )
            return self.__entity.set(self.__key, f"[I; {_values[0]}, {_values[1]}, {_values[2]}, {_values[3]}]")
        elif isinstance(value, EntityUUID):
            return self.__entity.set(self.__key, value.to_string())
        elif isinstance(value, Command):
            cmd = f"execute store result entity {self.__entity.get_target()} {self.__key} int 1 run {value.raw()}"
            return CustomCommand(["", "$"]["$" in cmd] + cmd)
        else:
            return self.__entity.set(self.__key, value)

    def get(self, scale: float | None = None) -> Command:
        """Obtém o valor do caminho NBT.

        Args:
            scale: fator de escala opcional
        """
        return self.__entity.get(self.__key, scale=scale)

    def merge(self, value: dict) -> Command:
        """Faz merge de dados no caminho NBT.

        Args:
            value: dict a ser mesclado
        """
        return self.__entity.merge(value)

    def remove(self) -> CustomCommand:
        """Remove o caminho NBT."""
        return self.__entity.remove(self.__key)

    def to_score(self, set: bool = False) -> "ScoreboardPlayer":
        """Converte o valor para um scoreboard player temporário.

        Args:
            set: se True, primeiro popula o storage com o valor atual

        Examples:

            >>> score = ed["Health"].to_score()
        """
        from datagen.function.commands.execute import Execute
        from datagen.utils.scoreboard.objective import ScoreboardObjective
        plr = (~ ScoreboardObjective.TEMP)["__entity_" + str(self.__entity.get_target()) + "." + str(self.__key)]
        if set:
            ~ (
                Execute()
                .STORE("result", "entity", self.__entity.get_target(), str(self.__key), "int", 1)  # type: ignore
                .RUN(self.get())
            )
        return plr

    def from_score(self, player: "ScoreboardPlayer") -> Command:
        """Copia um valor do scoreboard para o caminho NBT.

        Args:
            player: jogador do scoreboard
        """
        return CustomCommand(
            f"execute store result entity {self.__entity.get_target()} {self.__key} int 1 "
            f"run scoreboard players get {player} {player.objective}"
        )

    def to_data(self, into: "EntityDataValue | BlockEntityDataValue | DataStorageValue", scale: float = 1) -> Command:
        """Copia o valor para outro DataValue.

        Args:
            into: destino (EntityDataValue, BlockEntityDataValue ou DataStorageValue)
            scale: fator de escala
        """
        if isinstance(into, EntityDataValue):
            return CustomCommand(
                f"execute store result entity {into.get_entity().get_target()} {into.get_key()} int {scale} "
                f"run data get entity {self.__entity.get_target()} {self.__key}"
            )
        elif isinstance(into, BlockEntityDataValue):
            return CustomCommand(
                f"execute store result block {into.get_block_entity().get_pos()} {into.get_key()} int {scale} "
                f"run data get entity {self.__entity.get_target()} {self.__key}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"execute store result storage {into.storage._id_str()} {into.key} int {scale} "
                f"run data get entity {self.__entity.get_target()} {self.__key}"
            )

    def from_data(self, from_: "EntityDataValue | BlockEntityDataValue | DataStorageValue", scale: float = 1) -> Command:
        """Copia um valor de outro DataValue para este caminho.

        Args:
            from_: origem (EntityDataValue, BlockEntityDataValue ou DataStorageValue)
            scale: fator de escala
        """
        if isinstance(from_, EntityDataValue):
            return CustomCommand(
                f"execute store result entity {self.__entity.get_target()} {self.__key} int {scale} "
                f"run data get entity {from_.get_entity().get_target()} {from_.get_key()}"
            )
        elif isinstance(from_, BlockEntityDataValue):
            return CustomCommand(
                f"execute store result entity {self.__entity.get_target()} {self.__key} int {scale} "
                f"run data get block {from_.get_block_entity().get_pos()} {from_.get_key()}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"execute store result entity {self.__entity.get_target()} {self.__key} int {scale} "
                f"run data get storage {from_.storage._id_str()} {from_.key}"
            )

    def to_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        """Copia o valor para uma bossbar.

        Args:
            bossbar: identificador da bossbar
        """
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{id.get_path()}".lower()
        return CustomCommand(
            f"execute store result bossbar {_id} value int 1 "
            f"run data get entity {self.__entity.get_target()} {self.__key}"
        )

    def from_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        """Copia o valor de uma bossbar para o caminho NBT.

        Args:
            bossbar: identificador da bossbar
        """
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{id.get_path()}".lower()
        return CustomCommand(
            f"execute store result entity {self.__entity.get_target()} {self.__key} int 1 "
            f"run bossbar get {_id} value"
        )

    def set_into(self, into: "EntityDataValue | BlockEntityDataValue | DataStorageValue") -> Command:
        """Copia diretamente este valor para outro DataValue via data modify.

        Args:
            into: destino (EntityDataValue, BlockEntityDataValue ou DataStorageValue)
        """
        if isinstance(into, EntityDataValue):
            return CustomCommand(
                f"data modify entity {into.get_entity().get_target()} {into.get_key()} "
                f"set from entity {self.__entity.get_target()} {self.__key}"
            )
        elif isinstance(into, BlockEntityDataValue):
            return CustomCommand(
                f"data modify block {into.get_block_entity().get_pos()} {into.get_key()} "
                f"set from entity {self.__entity.get_target()} {self.__key}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"data modify storage {into.storage._id_str()} {into.key} "
                f"set from entity {self.__entity.get_target()} {self.__key}"
            )

    def __lshift__(self, other: "EntityDataValue.TAny | EntityData | BlockEntityData | DataStorage") -> Command:
        """Operador << para setar ou copiar valores.

        Examples:

            >>> ed["Health"] << 20.0
            >>> ed["Pos"] << other_ed["Pos"]
        """
        if isinstance(other, (EntityDataValue, BlockEntityDataValue, DataStorageValue)):
            return other.set_into(self)  # type: ignore
        elif isinstance(other, (EntityData, BlockEntityData, DataStorage)):
            return self.set(other)
        else:
            return self.set(other)


class BlockEntityDataValue[T]():
    """Valor encadeado de BlockEntityData.

    Permite operações em um caminho NBT específico de um block entity.

    Examples:

        >>> bed = BlockEntityData(BlockPosition(0, 5, 0))
        >>> bed["Items"].merge({...})
        >>> bed["CustomName"].remove()
    """

    type TAny = "T | FunctionMacroArgument | Identifier | Function | ScoreboardPlayer | BlockEntityDataValue | BlockEntityData | DataStorageValue | DataStorage | UUID | EntityUUID"  # type: ignore

    def __init__(self, block_entity: BlockEntityData, key: BlockEntityData.TKey) -> None:
        """Inicializa BlockEntityDataValue.

        Args:
            block_entity: BlockEntityData de origem
            key: caminho NBT
        """
        self.__block_entity = block_entity
        self.__key = key

    def get_block_entity(self) -> BlockEntityData:
        """Retorna o BlockEntityData de origem."""
        return self.__block_entity

    def get_key(self) -> BlockEntityData.TKey:
        """Retorna a chave/caminho NBT."""
        return self.__key

    def __getitem__(self, key: int | str | float | bool | Identifier | FunctionMacroArgument) -> "BlockEntityDataValue":
        """Acessa sub-caminho."""
        if isinstance(key, int):
            return BlockEntityDataValue(self.__block_entity, f"{self.__key}[{key}]")
        return BlockEntityDataValue(self.__block_entity, f"{self.__key}.{str(key)}")

    def set(self, value: "BlockEntityDataValue.TAny") -> Command:
        """Define o valor no caminho NBT.

        Args:
            value: valor a ser definido

        Examples:

            >>> bed["CustomName"].set('{"text":"Chest"}')
        """
        from datagen.function.function import Function
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(value, BlockEntityDataValue):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from block {value.get_block_entity().get_pos()} {value.get_key()}"
            )
        elif isinstance(value, EntityDataValue):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from entity {value.get_entity().get_target()} {value.get_key()}"
            )
        elif isinstance(value, DataStorageValue):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from storage {value.storage._id_str()} {value.key}"
            )
        elif isinstance(value, (Function, Identifier)):
            return self.__block_entity.set_from_function_return(self.__key, value)
        elif isinstance(value, ScoreboardPlayer):
            return self.__block_entity.set_from_score_player(self.__key, value)
        elif isinstance(value, FunctionMacroArgument):
            return self.__block_entity.set(self.__key, value)
        elif isinstance(value, EntityData):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from entity {value.get_target()}"
            )
        elif isinstance(value, BlockEntityData):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from block {value.get_pos()}"
            )
        elif isinstance(value, DataStorage):
            return CustomCommand(
                f"data modify block {self.__block_entity.get_pos()} {self.__key} "
                f"set from storage {value._id_str()}"
            )
        elif isinstance(value, UUID):
            _values: tuple[int, int, int, int] = (
                value.int >> 96 & 0xFFFFFFFF,
                value.int >> 64 & 0xFFFFFFFF,
                value.int >> 32 & 0xFFFFFFFF,
                value.int & 0xFFFFFFFF,
            )
            return self.__block_entity.set(self.__key, f"[I; {_values[0]}, {_values[1]}, {_values[2]}, {_values[3]}]")
        elif isinstance(value, EntityUUID):
            return self.__block_entity.set(self.__key, value.to_string())
        elif isinstance(value, Command):
            cmd = f"execute store result block {self.__block_entity.get_pos()} {self.__key} int 1 run {value.raw()}"
            return CustomCommand(["", "$"]["$" in cmd] + cmd)
        else:
            return self.__block_entity.set(self.__key, value)

    def get(self, scale: float | None = None) -> Command:
        """Obtém o valor do caminho NBT.

        Args:
            scale: fator de escala opcional
        """
        return self.__block_entity.get(self.__key, scale=scale)

    def merge(self, value: dict) -> Command:
        """Faz merge de dados no caminho NBT.

        Args:
            value: dict a ser mesclado
        """
        return self.__block_entity.merge(value)

    def remove(self) -> CustomCommand:
        """Remove o caminho NBT."""
        return self.__block_entity.remove(self.__key)

    def to_score(self, set: bool = False) -> "ScoreboardPlayer":
        """Converte o valor para um scoreboard player temporário.

        Args:
            set: se True, primeiro popula o storage com o valor atual
        """
        from datagen.function.commands.execute import Execute
        from datagen.utils.scoreboard.objective import ScoreboardObjective
        plr = (~ ScoreboardObjective.TEMP)["__block_" + str(self.__block_entity.get_pos()) + "." + str(self.__key)]
        if set:
            ~ (
                Execute()
                .STORE("result", "block", self.__block_entity.get_pos(), str(self.__key), "int", 1)  # type: ignore
                .RUN(self.get())
            )
        return plr

    def from_score(self, player: "ScoreboardPlayer") -> Command:
        """Copia um valor do scoreboard para o caminho NBT.

        Args:
            player: jogador do scoreboard
        """
        return CustomCommand(
            f"execute store result block {self.__block_entity.get_pos()} {self.__key} int 1 "
            f"run scoreboard players get {player} {player.objective}"
        )

    def to_data(self, into: "EntityDataValue | BlockEntityDataValue | DataStorageValue", scale: float = 1) -> Command:
        """Copia o valor para outro DataValue.

        Args:
            into: destino
            scale: fator de escala
        """
        if isinstance(into, EntityDataValue):
            return CustomCommand(
                f"execute store result entity {into.get_entity().get_target()} {into.get_key()} int {scale} "
                f"run data get block {self.__block_entity.get_pos()} {self.__key}"
            )
        elif isinstance(into, BlockEntityDataValue):
            return CustomCommand(
                f"execute store result block {into.get_block_entity().get_pos()} {into.get_key()} int {scale} "
                f"run data get block {self.__block_entity.get_pos()} {self.__key}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"execute store result storage {into.storage._id_str()} {into.key} int {scale} "
                f"run data get block {self.__block_entity.get_pos()} {self.__key}"
            )

    def from_data(self, from_: "EntityDataValue | BlockEntityDataValue | DataStorageValue", scale: float = 1) -> Command:
        """Copia um valor de outro DataValue para este caminho.

        Args:
            from_: origem
            scale: fator de escala
        """
        if isinstance(from_, EntityDataValue):
            return CustomCommand(
                f"execute store result block {self.__block_entity.get_pos()} {self.__key} int {scale} "
                f"run data get entity {from_.get_entity().get_target()} {from_.get_key()}"
            )
        elif isinstance(from_, BlockEntityDataValue):
            return CustomCommand(
                f"execute store result block {self.__block_entity.get_pos()} {self.__key} int {scale} "
                f"run data get block {from_.get_block_entity().get_pos()} {from_.get_key()}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"execute store result block {self.__block_entity.get_pos()} {self.__key} int {scale} "
                f"run data get storage {from_.storage._id_str()} {from_.key}"
            )

    def to_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        """Copia o valor para uma bossbar.

        Args:
            bossbar: identificador da bossbar
        """
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{id.get_path()}".lower()
        return CustomCommand(
            f"execute store result bossbar {_id} value int 1 "
            f"run data get block {self.__block_entity.get_pos()} {self.__key}"
        )

    def from_bossbar(self, bossbar: "Identifier | BossBar") -> Command:
        """Copia o valor de uma bossbar para o caminho NBT.

        Args:
            bossbar: identificador da bossbar
        """
        from datagen.function.commands.bossbar import BossBar
        if isinstance(bossbar, BossBar):
            id = bossbar._id
        else:
            id = bossbar
        _id = f"{id.get_namespace()}:{id.get_path()}".lower()
        return CustomCommand(
            f"execute store result block {self.__block_entity.get_pos()} {self.__key} int 1 "
            f"run bossbar get {_id} value"
        )

    def set_into(self, into: "EntityDataValue | BlockEntityDataValue | DataStorageValue") -> Command:
        """Copia diretamente este valor para outro DataValue via data modify.

        Args:
            into: destino
        """
        if isinstance(into, EntityDataValue):
            return CustomCommand(
                f"data modify entity {into.get_entity().get_target()} {into.get_key()} "
                f"set from block {self.__block_entity.get_pos()} {self.__key}"
            )
        elif isinstance(into, BlockEntityDataValue):
            return CustomCommand(
                f"data modify block {into.get_block_entity().get_pos()} {into.get_key()} "
                f"set from block {self.__block_entity.get_pos()} {self.__key}"
            )
        else:  # DataStorageValue
            return CustomCommand(
                f"data modify storage {into.storage._id_str()} {into.key} "
                f"set from block {self.__block_entity.get_pos()} {self.__key}"
            )

    def __lshift__(self, other: "BlockEntityDataValue.TAny | EntityData | BlockEntityData | DataStorage") -> Command:
        """Operador << para setar ou copiar valores."""
        if isinstance(other, (EntityDataValue, BlockEntityDataValue, DataStorageValue)):
            return other.set_into(self)  # type: ignore
        elif isinstance(other, (EntityData, BlockEntityData, DataStorage)):
            return self.set(other)
        else:
            return self.set(other)
