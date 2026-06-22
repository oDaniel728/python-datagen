from collections.abc import Iterable

from datagen.utils.repr.appliedstatuseffect import AppliedStatusEffect
from datagen.utils.repr.attribute import Attribute
from datagen.utils.repr.position3 import Position3
from datagenpp.extras.repr.entitysettings import EntitySettings
from datagen.types.util.reprs import *

class MobEntitySettings(EntitySettings):
    def __init__(self) -> None:
        super().__init__()

    def with_absorption_amount(self, value: float):
        self.nbt["AbsorptionAmount"] = value
        return self

    def with_active_effects(self, value: Iterable[AppliedStatusEffect]):
        self.nbt["ActiveEffects"] = [effect.to_dict() for effect in value]
        return self
    
    def with_attributes(self, value: None): # TODO!
        self.nbt["Attributes"] = value
        return self

    def with_can_pick_up_loot(self, value: boolean):
        self.nbt["CanPickUpLoot"] = int(value)
        return self

    def with_death_time(self, value: short):
        self.nbt["DeathTime"] = value
        return self
    
    def with_fall_flying(self, value: boolean):
        self.nbt["FallFlying"] = int(value)
        return self
    
    def with_hurt_by_timestamp(self, value: int):
        self.nbt["HurtByTimestamp"] = value
        return self

    def with_hurt_time(self, value: short):
        self.nbt["HurtTime"] = value
        return self
    
    def with_left_handed(self, value: boolean):
        self.nbt["LeftHanded"] = int(value)
        return self

    def with_no_ai(self, value: boolean):
        self.nbt["NoAI"] = int(value)
        return self
    
    def with_persistance_required(self, value: boolean):
        self.nbt["PersistenceRequired"] = int(value)
        return self

    def with_sleeping_x(self, value: int):
        self.nbt["SleepingX"] = value
        return self
    
    def with_sleeping_y(self, value: int):
        self.nbt["SleepingY"] = value
        return self
    
    def with_sleeping_z(self, value: int):
        self.nbt["SleepingZ"] = value
        return self
    
    def with_sleeping_pos(self, pos: Position3):
        self.nbt["SleepingX"] = pos.x
        self.nbt["SleepingY"] = pos.y
        self.nbt["SleepingZ"] = pos.z
        return self
    
    def with_team(self, value: str):
        self.nbt["Team"] = value
        return self