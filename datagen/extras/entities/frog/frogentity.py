from typing import Self

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.entitytype import EntityType


class FrogEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.FROG)

    VARIANT_TEMPERATE = Identifier.of("minecraft", "temperate")
    VARIANT_COLD = Identifier.of("minecraft", "cold")
    VARIANT_WARM = Identifier.of("minecraft", "warm")

    def with_variant(self, variant: Identifier) -> "Self":
        """
        ID of the frog's variant.
        Represents the minecraft:frog/variant component.
        Common values: FrogEntity.VARIANT_TEMPERATE, FrogEntity.VARIANT_COLD, FrogEntity.VARIANT_WARM.
        """
        self.properties["Variant"] = variant
        return self