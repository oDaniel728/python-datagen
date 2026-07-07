from typing import Self

from datagen.extras.entities.baseprojectileentity import BaseProjectileEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class Potion(BaseProjectileEntity):
    def __init__(self):
        super().__init__(EntityTypes.AREA_EFFECT_CLOUD)

    def with_item(self, value: ItemStack) -> "Self":
        self.properties["Item"] = value
        return self