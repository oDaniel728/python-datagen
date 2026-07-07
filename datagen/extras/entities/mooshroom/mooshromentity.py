from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class MooshroomEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.MOOSHROOM)

    def with_stew_effects(self, value: list[dict]) -> "MooshroomEntity":
        self.properties["stew_effects"] = value
        return self

    def with_type(self, value: str) -> "MooshroomEntity":
        self.properties["Type"] = value
        return self