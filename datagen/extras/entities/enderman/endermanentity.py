from typing import Self

from datagen.extras.entities.angerentities import AngerEntities
from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.block import Block


class EndermanEntity(BaseEntity, MobEntity, AngerEntities):
    def __init__(self):
        super().__init__(EntityTypes.ENDERMAN)

    def with_carried_block_state(self, block: Block) -> "Self":
        """
        The block state of the block the enderman is carrying.
        If the enderman is not carrying a block, this property is not present.
        """
        self.properties["carriedBlockState"] = block.to_state()
        return self