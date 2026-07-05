from typing import Self

from datagen.extras.entities.display.displayentity import DisplayEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType


class BlockDisplayEntity(DisplayEntity):
    def __init__(self):
        super().__init__(EntityTypes.BLOCK_DISPLAY)

    def with_block_state(self, block: Block) -> "Self":
        self.properties["block_state"] = block.to_state()
        return self