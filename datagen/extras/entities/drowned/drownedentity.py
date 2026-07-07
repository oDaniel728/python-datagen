from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class DrownedEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ZOMBIE)

    def with_can_break_doors(self, can_break_doors: bool) -> "DrownedEntity":
        """
        Whether or not the drowned can break doors.
        If true, the drowned can break doors and will do so when pathfinding to a target.
        """
        self.properties["CanBreakDoors"] = can_break_doors
        return self
    
    def with_drowned_conversion_time(self, drowned_conversion_time: int) -> "DrownedEntity":
        """
        Number of ticks until the drowned converts to a zombie.
        Conversion occurs at 0 and this timer gets reset to a new random value between 300 and 600.
        """
        self.properties["DrownedConversionTime"] = drowned_conversion_time
        return self
    
    def with_in_water_time(self, in_water_time: int) -> "DrownedEntity":
        """
        Number of ticks the drowned has been in water.
        This timer resets to 0 when the drowned is not in water.
        """
        self.properties["InWaterTime"] = in_water_time
        return self

    def with_is_baby(self, is_baby: bool) -> "DrownedEntity":
        """
        Whether or not the drowned is a baby.
        If true, the drowned will be a baby and will have a smaller hitbox and move faster.
        """
        self.properties["IsBaby"] = is_baby
        return self