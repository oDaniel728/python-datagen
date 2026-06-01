from typing import Any

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item

class Block[T: ToDict | dict[str, Any]](Item[T]):
    def __init__(self, id: Identifier, nbt: T) -> None:
        super().__init__(id, nbt)