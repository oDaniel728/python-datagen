from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class PiglinEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.PIGLIN)

    def with_cannot_hunt(self, value: bool) -> "PiglinEntity":
        self.properties["CannotHunt"] = value
        return self

    def with_is_baby(self, value: bool) -> "PiglinEntity":
        self.properties["IsBaby"] = value
        return self

    def with_is_immune_to_zombification(self, value: bool) -> "PiglinEntity":
        self.properties["IsImmuneToZombification"] = value
        return self

    def with_time_in_overworld(self, value: int) -> "PiglinEntity":
        self.properties["TimeInOverworld"] = value
        return self