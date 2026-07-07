from typing import Self

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class EnderDragonEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ENDER_DRAGON)

    def with_dragon_death_time(self, dragon_death_time: int) -> "Self":
        self.properties["DragonDeathTime"] = dragon_death_time
        return self
    
    PHASE_CIRCLING = 0
    PHASE_STRAFING = 1
    PHASE_FLYING_TO_PORTAL = 2
    PHASE_LANDING_ON_PORTAL = 3
    PHASE_TAKING_OFF_FROM_PORTAL = 4
    PHASE_BREATH_ATTACK = 5
    PHASE_LOOKING_FOR_PLAYER = 6
    PHASE_LANDED = 7
    PHASE_CHARGING_PLAYER = 8
    PHASE_FLYING_TO_DIE = 9
    PHASE_HOVERING = 10

    def with_dragon_phase(self, value: int) -> "Self":
        self.properties["DragonPhase"] = value
        return self
    
    def with_sitting_damage_received(self, value: float) -> "Self":
        self.properties["sitting_damage_received"] = value
        return self