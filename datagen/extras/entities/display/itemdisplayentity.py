from typing import Literal, Self

from datagen.extras.entities.display.displayentity import DisplayEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class ItemDisplayEntity(DisplayEntity):
    def __init__(self):
        super().__init__(EntityTypes.ITEM_DISPLAY)

    def with_item(self, stack: ItemStack) -> "Self":
        self.properties["item"] = stack.to_dict()
        return self
    
    _TItemDisplayModel = Literal["none", "thirdperson_lefthand", "thirdperson_righthand", "firstperson_lefthand", "firstperson_righthand", "head", "gui", "ground", "fixed"]
    def with_item_display(self, model: _TItemDisplayModel = 'none') -> "Self":
        self.properties["item_display"] = model
        return self