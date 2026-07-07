from uuid import UUID

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.identifier import Identifier


class FoxEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.FOX)

    def with_crouching(self, crouching: bool) -> "FoxEntity":
        """
        Whether the fox is crouching.
        """
        self.properties["Crouching"] = crouching
        return self

    def with_sitting(self, sitting: bool) -> "FoxEntity":
        """
        Whether the fox is sitting.
        """
        self.properties["Sitting"] = sitting
        return self

    def with_sleeping(self, sleeping: bool) -> "FoxEntity":
        """
        Whether the fox is sleeping.
        """
        self.properties["Sleeping"] = sleeping
        return self

    def with_trusted(self, trusted: list[UUID]) -> "FoxEntity":
        """
        A list of players that the fox trusts.
        For a list with more than 2 elements, only the first and the last are considered.
        Each UUID is stored as four ints.
        """
        self.properties["Trusted"] = trusted
        return self

    TYPE_RED = Identifier.of("minecraft", "red")
    TYPE_SNOW = Identifier.of("minecraft", "snow")

    def with_type(self, type: Identifier) -> "FoxEntity":
        """
        ID of the fox's type (variant).
        Represents the minecraft:fox/variant component.
        Common values: FoxEntity.TYPE_RED, FoxEntity.TYPE_SNOW.
        """
        self.properties["Type"] = type
        return self
