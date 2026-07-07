from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class IronGolemEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.IRON_GOLEM)

    def with_player_created(self, value: bool) -> "IronGolemEntity":
        self.properties["PlayerCreated"] = value
        return self