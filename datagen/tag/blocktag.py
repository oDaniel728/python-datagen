from typing import Iterable

from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item


class BlockTag(Tag[Block]):
    def __init__(self, id: Identifier, values: Iterable[Block] = [], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Block