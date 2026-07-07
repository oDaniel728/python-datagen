from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PhantomEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.PHANTOM)

    def with_size(self, value: int) -> "PhantomEntity":
        self.properties["size"] = value
        return self

    def with_anchor_pos(self, value: list[int]) -> "PhantomEntity":
        self.properties["anchor_pos"] = value
        return self