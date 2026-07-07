from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class OcelotEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.OCELOT)

    def with_trusting(self, value: bool) -> "OcelotEntity":
        self.properties["Trusting"] = value
        return self