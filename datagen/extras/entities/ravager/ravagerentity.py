from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.extras.entities.spawnableinraidsentities import SpawnableInRaidsEntities
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class RavagerEntity(BaseEntity, MobEntity, SpawnableInRaidsEntities):
    def __init__(self):
        super().__init__(EntityTypes.RAVAGER)

    def with_attack_tick(self, value: int) -> "RavagerEntity":
        self.properties["AttackTick"] = value
        return self

    def with_roar_tick(self, value: int) -> "RavagerEntity":
        self.properties["RoarTick"] = value
        return self

    def with_stun_tick(self, value: int) -> "RavagerEntity":
        self.properties["StunTick"] = value
        return self