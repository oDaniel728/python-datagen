from typing import Self

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.types.util.reprs import *

class CreeperEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.CREEPER)

    def with_explosion_radius(self, value: byte = 3) -> "Self":
        """
        The radius of the creeper's explosion.
        """
        self.properties["ExplosionRadius"] = value
        return self
    
    def with_fuse_time(self, value: short = 30) -> "Self":
        """
        The number of ticks until the creeper explodes after it starts to ignite.
        """
        self.properties["Fuse"] = value
        return self
    
    def with_ignited(self, value: bool = False) -> "Self":
        """
        Whether or not the creeper is currently ignited.
        """
        self.properties["ignited"] = int(value)
        return self
    
    def with_powered(self, value: bool = False) -> "Self":
        """
        Whether or not the creeper is powered (charged).
        """
        self.properties["powered"] = int(value)
        return self