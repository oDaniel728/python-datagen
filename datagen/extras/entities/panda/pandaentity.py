from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PandaEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.PANDA)

    def with_hidden_gene(self, value: str) -> "PandaEntity":
        self.properties["HiddenGene"] = value
        return self

    def with_main_gene(self, value: str) -> "PandaEntity":
        self.properties["MainGene"] = value
        return self