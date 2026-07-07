from typing import Literal

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class ArmadilloEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ARMADILLO)

    def with_scute_time(self, scute_time: int) -> "ArmadilloEntity":
        self.properties["scute_time"] = scute_time
        return self
    
    _TState = Literal["idle", "scared", "unrolling"]
    def with_state(self, state: _TState) -> "ArmadilloEntity":
        self.properties["state"] = state
        return self