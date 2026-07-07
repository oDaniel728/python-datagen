from typing import Self

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class DolphinEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.DOLPHIN)

    def with_moistness(self, moisture: int) -> "Self":
        """
        The number of ticks since the dolphin was last in water.
        When this reaches 2400, the dolphin will start to take damage from being out of water.
        """
        self.properties["Moistness"] = moisture
        return self
    
    def with_got_fish(self, got_fish: bool) -> "Self":
        """
        Whether or not the dolphin has recently eaten a fish.
        If true, the dolphin will swim faster and jump higher for 600 ticks (30 seconds).
        """
        self.properties["GotFish"] = int(got_fish)
        return self