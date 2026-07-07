from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class AxolotlEntity(BaseEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.AXOLOTL)

    def with_from_bucket(self, from_bucket: bool):
        self.properties['FromBucket'] = from_bucket
        return self

    VARIANT_LUCY = 0
    VARIANT_WILD = 1
    VARIANT_GOLD = 2
    VARIANT_CYAN = 3
    VARIANT_BLUE = 4
    
    def with_variant(self, variant: int):
        self.properties['Variant'] = variant
        return self