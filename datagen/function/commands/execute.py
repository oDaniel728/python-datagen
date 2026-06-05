from typing import Any, Callable, Literal, Self, overload

from datagen.function.commands.command import Command
from datagen.function.commands.data.datastorage import DataStorage
from datagen.function.function import Function
from datagen.types.util.min import Range
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.biome import Biome
from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.repr.itempath import ItemPath
from datagen.utils.repr.position3 import Position3
from datagen.utils.scoreboard.player import ScoreboardPlayer

type IDontCare = Any

class _ConditionBuilder():
    def __init__(self, parent: "Execute", prefix: str = "{self._prefix}"):
        self._parent = parent
        self._prefix = prefix

    def block(self, block: Block, at: BlockPosition):
        self._parent.chunks.append(f"{self._prefix} block {at} {block.id}")
        return self

    _TBlocksCondition = Literal["all", "masked"]
    def blocks(self, start: BlockPosition, end: BlockPosition, destination: BlockPosition, condition: _TBlocksCondition = "all"):
        self._parent.chunks.append(f"{self._prefix} blocks {start} {end} {destination} {condition}")
        return self

    def entity(self, target: TargetSelector):
        self._parent.chunks.append(f"{self._prefix} entity {target}")    
        return self

    _TScoreComparison = Literal["=", "<", ">", "<=", ">="]

    @overload
    def score(self, target: ScoreboardPlayer, comparison: _TScoreComparison, other: ScoreboardPlayer, /) -> Self: ...
    @overload
    def score(self, target: ScoreboardPlayer, comparison: Literal["matches"], value: Range | int, /) -> Self: ...
    
    def score(self, *args) -> Self:
        player: ScoreboardPlayer
        comparison: str
        value: ScoreboardPlayer | Range | int

        player, comparison, value = args

        _value = str(value)
        _player = f"{player.name} {player.objective}"
        if isinstance(value, ScoreboardPlayer):
            _value = f"{value.name} {value.objective}"

        self._parent.chunks.append(f"{self._prefix} score {_player} {comparison} {_value}")
        return self

    @overload
    def data(self, 
        type: Literal["block"], 
        pos: BlockPosition, 
        path: str,
        /
    ) -> Self: ...
    @overload
    def data(self, 
        type: Literal["entity"], 
        target: TargetSelector, 
        path: str,
        /
    ) -> Self: ...
    @overload
    def data(self, 
        type: Literal["storage"], 
        storage: "DataStorage | Identifier", 
        path: str,
        /
    ) -> Self: ...

    def data(self, *args) -> Self:
        type: str = args[0]
        if type == "block":
            _, pos, path = args
            self._parent.chunks.append(f"{self._prefix} data block {pos} {path}")
        elif type  == "entity":
            _, target, path = args
            self._parent.chunks.append(f"{self._prefix} data entity {target} {path}")
        elif type == "storage":
            _, storage, path = args
            storage_id = storage.id if isinstance(storage, DataStorage) else storage
            self._parent.chunks.append(f"{self._prefix} data storage {storage_id} {path}")
        return self

    def dimension(self, dimension: Identifier) -> Self:
        self._parent.chunks.append(f"{self._prefix} dimension {dimension}")
        return self

    def predicate(self, predicate: Identifier) -> Self:
        self._parent.chunks.append(f"{self._prefix} predicate {predicate}")
        return self

    def loaded(self, location: BlockPosition) -> Self:
        self._parent.chunks.append(f"{self._prefix} loaded {location}")
        return self

    def function(self, function: "Identifier | Function") -> Self:
        func_id = function.id if isinstance(function, Function) else function
        self._parent.chunks.append(f"{self._prefix} function {func_id}")
        return self

    @overload
    def items(self, 
        type: Literal["block"], 
        pos: BlockPosition, 
        path: ItemPath, 
        item: Item,
        /
    ) -> Self: ...

    @overload
    def items(self,
        type: Literal["entity"], 
        target: TargetSelector,
        path: ItemPath,
        item: Item,
        /
    ) -> Self: ...

    def items(self, *args) -> Self:
        type: str = args[0]
        if type == "block":
            _, pos, path, item = args
            self._parent.chunks.append(f"{self._prefix} items block {pos} {path} {item.id}")
        elif type == "entity":
            _, target, path, item = args
            self._parent.chunks.append(f"{self._prefix} items entity {target} {path} {item.id}")
        return self

    def biome(self, biome: Biome) -> Self:
        self._parent.chunks.append(f"{self._prefix} biome {biome.id}")
        return self

class Execute(Command):
    def __init__(self):
        super().__init__()

        self.condition_builder = _ConditionBuilder(self, prefix="if")
        self.unless_condition_builder = _ConditionBuilder(self, prefix="unless")
        self.chunks = list[str]()

    def IF(self, supplier: Callable[[_ConditionBuilder], IDontCare]) -> "Execute":
        supplier(self.condition_builder)
        return self

    def RUN(self, command: Command | Function | Identifier) -> "Execute":
        if isinstance(command, Command):
            self.chunks.append("run " + command.raw())
        elif isinstance(command, Function):
            self.chunks.append(f"run function {command.id}")
        elif isinstance(command, Identifier):
            self.chunks.append(f"run function {command}")
        else:
            raise ValueError("Invalid command type")
        return self

    def AS(self, target: TargetSelector) -> "Execute":
        self.chunks.append(f"as {target.to_string()}")
        return self
    
    def AT(self, target: TargetSelector) -> "Execute":
        self.chunks.append(f"at {target.to_string()}")
        return self
    
    _TAlignAxes = Literal[
        "x", "y", "z", 
        "xy", "xz",
        "yx", "yz",
        "zx", "zy",
        "xyz"
    ]
    def ALIGN(self, axes: _TAlignAxes) -> "Execute":
        self.chunks.append(f"align {axes}")
        return self

    _TAnchored = Literal["eyes", "feet"]
    def ANCHORED(self, anchored: _TAnchored) -> "Execute":
        self.chunks.append(f"anchored {anchored}")
        return self
    
    @overload
    def FACING(self,
        pos: Position3,
        /
    ) -> "Execute": ...
    @overload
    def FACING(self,
        target: TargetSelector,
        facing_anchor: _TAnchored,
        /
    ) -> "Execute": ...

    def FACING(self, *args) -> "Execute":
        if len(args) == 1:
            pos: Position3 = args[0]
            self.chunks.append(f"facing {pos.to_string()}")
        elif len(args) == 2:
            target: TargetSelector = args[0]
            facing_anchor: Execute._TAnchored = args[1]
            self.chunks.append(f"facing entity {target.to_string()} {facing_anchor}")
        else:
            raise ValueError("Invalid arguments for FACING")
        return self
    
    def IN(self, dimension: Identifier) -> "Execute":
        self.chunks.append(f"in {dimension}")
        return self

    _TOn = Literal[
        "attacker", 
        "controller", 
        "leasher",
        "origin",
        "owner",
        "passengers",
        "target",
        "vehicle"
    ]    
    def ON(self, on: _TOn) -> "Execute":
        self.chunks.append(f"on {on}")
        return self
    
    def POSITIONED(self, pos: Position3) -> "Execute":
        self.chunks.append(f"positioned {pos.to_string()}")
        return self

    def POSITIONED_AS(self, target: TargetSelector) -> "Execute":
        self.chunks.append(f"positioned as {target.to_string()}")
        return self
    
    _TPositionedOver = Literal[
        "motion_blocking",
        "motion_blocking_no_leaves",
        "ocean_floor",
        "world_surface"
    ]
    def POSITIONED_OVER(self, target: _TPositionedOver) -> "Execute":
        self.chunks.append(f"positioned over {target}")
        return self
    
    def ROTATED(self, target: TargetSelector) -> "Execute":
        self.chunks.append(f"rotated as {target.to_string()}")
        return self

    _TStoreType = Literal["block", "entity", "storage", "bossbar"]
    _TStoreResultType = Literal["result", "success"]
    _TStoreDataType = Literal["int", "float", "long", "short", "byte", "double"]

    @overload
    def STORE(self,
        result_type: _TStoreResultType,
        type: Literal["block"],
        pos: BlockPosition,
        path: str,
        data_type: _TStoreDataType = "int",
        scale: float = 1.0,
        /
    ) -> "Execute": ...
    @overload
    def STORE(self,
        result_type: _TStoreResultType,
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        data_type: _TStoreDataType = "int",
        scale: float = 1.0,
        /
    ) -> "Execute": ...
    @overload
    def STORE(self,
        result_type: _TStoreResultType,
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        data_type: _TStoreDataType = "int",
        scale: float = 1.0,
        /
    ) -> "Execute": ...
    @overload
    def STORE(self,
        result_type: _TStoreResultType,
        type: Literal["bossbar"],
        target: Identifier,
        value: Literal["value", "max"],
        /
    ) -> "Execute": ...

    def STORE(self, *args) -> "Execute":
        result_type: str = args[0]
        type: str = args[1]

        if type == "block":
            _, result_type, _, pos, path, data_type, scale = args
            self.chunks.append(f"store {result_type} block {pos} {path} {data_type} {scale}")
        elif type == "entity":
            _, result_type, _, target, path, data_type, scale = args
            self.chunks.append(f"store {result_type} entity {target} {path} {data_type} {scale}")
        elif type == "storage":
            _, result_type, _, target, path, data_type, scale = args
            target_id = target.id if isinstance(target, DataStorage) else target
            self.chunks.append(f"store {result_type} storage {target_id} {path} {data_type} {scale}")
        elif type == "bossbar":
            _, result_type, _, target, value = args
            self.chunks.append(f"store {result_type} bossbar {target} {value}")
        else:
            raise ValueError("Invalid store type")
        
        return self
    
    def SUMMON(self, entity: Identifier | EntityType) -> "Execute":
        entity_id = entity.id if isinstance(entity, EntityType) else entity
        self.chunks.append(f"summon {entity_id}")
        return self
    
    def UNLESS(self, supplier: Callable[[_ConditionBuilder], IDontCare]) -> "Execute":
        supplier(self.unless_condition_builder)
        return self

    def to_string(self) -> str:
        return self.auto_macro("execute " + " ".join(self.chunks))
    
    def copy(self) -> "Execute":
        new = Execute()
        new.chunks = self.chunks.copy()
        return new