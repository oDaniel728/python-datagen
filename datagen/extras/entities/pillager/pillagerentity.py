from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PillagerEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.PILLAGER)

    def with_inventory(self, value: list) -> "PillagerEntity":
        self.properties["Inventory"] = value
        return self