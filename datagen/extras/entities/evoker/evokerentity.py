from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.extras.entities.spawnableinraidsentities import SpawnableInRaidsEntities
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class EvokerEntity(BaseEntity, MobEntity, SpawnableInRaidsEntities):
    def __init__(self):
        super().__init__(EntityTypes.EVOKER)

    def with_spell_ticks(self, spell_ticks: int) -> "EvokerEntity":
        """
        The number of ticks until the evoker casts its next spell.
        """
        self.properties["SpellTicks"] = spell_ticks
        return self