from typing import Any, override

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item

class __Settings__(Item.Settings):
    def __init__(self) -> None:
        super().__init__()

class Block[T: __Settings__](Item[T]):    
    class Settings(__Settings__):
        def __init__(self) -> None:
            super().__init__()

    def __init__(self, id: Identifier, nbt: T | dict) -> None:
        super().__init__(id, nbt)

    def with_settings[U: __Settings__](self, setting: U) -> "Block[U]": # type: ignore
        return Block[U](self.id, setting)
