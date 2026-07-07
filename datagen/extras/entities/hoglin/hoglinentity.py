from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class HoglinEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.HOGLIN)

    def with_cannot_be_hunted(self, value: bool) -> "HoglinEntity":
        self.properties["CannotBeHunted"] = value
        return self

    def with_is_immune_to_zombification(self, value: bool) -> "HoglinEntity":
        self.properties["IsImmuneToZombification"] = value
        return self

    def with_time_in_overworld(self, value: int) -> "HoglinEntity":
        self.properties["TimeInOverworld"] = value
        return self