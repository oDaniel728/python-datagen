from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PufferfishEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.PUFFERFISH)

    def with_from_bucket(self, value: bool) -> "PufferfishEntity":
        self.properties["FromBucket"] = value
        return self

    def with_puff_state(self, value: int) -> "PufferfishEntity":
        self.properties["PuffState"] = value
        return self