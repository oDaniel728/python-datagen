from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class HuskEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.HUSK)

    def with_can_break_doors(self, value: bool) -> "HuskEntity":
        self.properties["CanBreakDoors"] = value
        return self

    def with_drowned_conversion_time(self, value: int) -> "HuskEntity":
        self.properties["DrownedConversionTime"] = value
        return self

    def with_in_water_time(self, value: int) -> "HuskEntity":
        self.properties["InWaterTime"] = value
        return self

    def with_is_baby(self, value: bool) -> "HuskEntity":
        self.properties["IsBaby"] = value
        return self