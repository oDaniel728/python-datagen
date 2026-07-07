from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class GhastEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.GHAST)

    def with_explosion_power(self, explosion_power: int) -> "GhastEntity":
        """
        The radius of the explosion created by the fireballs the ghast fires.
        Default value is 1.
        """
        self.properties["ExplosionPower"] = explosion_power
        return self
