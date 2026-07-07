from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class MagmaCubeEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.MAGMA_CUBE)

    def with_size(self, value: int) -> "MagmaCubeEntity":
        self.properties["Size"] = value
        return self