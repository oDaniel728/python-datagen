from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class BatEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.BAT)

    def with_bat_flaps(self, flaps: bool):
        self.properties["BatFlaps"] = flaps
        return self