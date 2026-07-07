from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class RabbitEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.RABBIT)

    def with_more_carrot_ticks(self, value: int) -> "RabbitEntity":
        self.properties["MoreCarrotTicks"] = value
        return self

    def with_rabbit_type(self, value: int) -> "RabbitEntity":
        self.properties["RabbitType"] = value
        return self