from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PiglinBruteEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.PIGLIN_BRUTE)

    def with_is_immune_to_zombification(self, value: bool) -> "PiglinBruteEntity":
        self.properties["IsImmuneToZombification"] = value
        return self

    def with_time_in_overworld(self, value: int) -> "PiglinBruteEntity":
        self.properties["TimeInOverworld"] = value
        return self