from abc import ABC, abstractmethod
import json
from typing import Any, Literal, Self, override

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item

class __Settings__(Item.Settings, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_block_state(self) -> dict: ...
    @abstractmethod
    def get_block_entity_data(self) -> dict: ...

    def to_dict(self) -> dict:
        return {
            "block_state": self.get_block_state(),
            "block_entity_data": self.get_block_entity_data()
        }
    
    def get_components(self) -> dict:
        return self.to_dict()

class Block[T: __Settings__](Item[T]):  


    _TDirection = Literal["down", "up", "north", "south", "west", "east"]
    instances = dict[Identifier, "Block"]()  
    class Settings(__Settings__):
        def __init__(self) -> None:
            super().__init__()

        def to_dict(self) -> dict[str, Any]:
            return super().to_dict()

    class BlockDefaultSettings(Settings):
        def __init__(self) -> None:
            super().__init__()

        def get_block_state(self) -> dict:
            return {}

        def get_block_entity_data(self) -> dict:
            return {}
    def __init__(self, id: Identifier, nbt: T | dict = {}) -> None:
        super().__init__(id, nbt)
        self.nbt = nbt if not isinstance(nbt, dict) else self.BlockDefaultSettings()
        Block.instances[id] = self

    def with_settings[U: __Settings__](self, setting: U) -> "Block[U]": # type: ignore
        return Block[U](self.id, setting)

    @staticmethod
    def _encode(val: Any) -> Any:
        if isinstance(val, ToDict):
            return Block._encode(val.to_dict())
        elif isinstance(val, dict):
            return {Block._encode(k): Block._encode(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [Block._encode(v) for v in val]
        elif isinstance(val, tuple):
            return tuple(Block._encode(v) for v in val)
        elif isinstance(val, set):
            return {Block._encode(v) for v in val}
        elif isinstance(val, Identifier):
            return ~val
        elif isinstance(val, Item):
            return ~val.id
        elif isinstance(val, Block):
            return ~val.id
        elif isinstance(val, (str, int, float, bool)):
            return json.dumps(val)
        else:
            raise TypeError(f"Unsupported type for SNBT serialization: {type(val)}")
        return val

    def __str__(self) -> str:
        # <id>[state]{entity}
        state_str = ",".join(f"{k}={v}" for k, v in self._encode(self.nbt.get_block_state()).items())
        entity_str = ",".join(f"{k}:{v}" for k, v in self._encode(self.nbt.get_block_entity_data()).items())
        return f"{~self.id}[{state_str}]{{{entity_str}}}"
    
    def at(self, pos: BlockPosition):
        from datagen.utils.repr.placeableblock import PlaceableBlock
        return PlaceableBlock(self.id, self.nbt, pos) # type: ignore