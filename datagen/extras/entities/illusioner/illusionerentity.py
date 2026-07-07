from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class IllusionerEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ILLUSIONER)

    def with_spell_ticks(self, value: int) -> "IllusionerEntity":
        self.properties["SpellTicks"] = value
        return self