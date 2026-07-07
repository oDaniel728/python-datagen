from typing import Self
from uuid import UUID

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.types.util.reprs import tuple4

class CamelEntity(BaseEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.CAMEL)

    def with_bred(self, bred: bool) -> "Self":
        self.properties["Bred"] = bred
        return self

    def with_eating_haystack(self, eating_haystack: bool) -> "Self":
        self.properties["EatingHaystack"] = eating_haystack
        return self
    
    def with_owner(self, value: tuple4[int] | list[int] | UUID) -> "Self":
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Owner"] = value
        return self

    def with_tame(self, tame: bool) -> "Self":
        self.properties["Tame"] = tame
        return self
    
    def with_temper(self, temper: int) -> "Self":
        self.properties["Temper"] = temper
        return self
    
    def with_last_pose_tick(self, last_pose_tick: int) -> "Self":
        self.properties["LastPoseTick"] = last_pose_tick
        return self