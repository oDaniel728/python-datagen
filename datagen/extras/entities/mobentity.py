from typing import Self
from uuid import UUID

from datagen.entityteam import EntityTeam
from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entityattribute import EntityAttribute
from datagen.loot_table.loot_table import LootTable
from datagen.types.util.holder import Holder
from datagen.utils.converters import IdentifierConverter
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.appliedstatuseffect import AppliedStatusEffect
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.position3 import Position3
from datagen.types.util.reprs import *


class MobEntity(BaseEntity):
    def __init__(self, type: EntityType):
        super().__init__(type)

    def with_absorption_amount(self, value: float) -> "Self":
        self.properties["AbsorptionAmount"] = value
        return self
    
    def with_active_effects(self, values: list[AppliedStatusEffect]) -> "Self":
        self.properties["ActiveEffects"] = list(values)
        return self
    
    def add_active_effect(self, value: AppliedStatusEffect) -> "Self":
        self.properties.setdefault("ActiveEffects", []).append(value)
        return self
    
    def with_attributes(self, values: list[EntityAttribute]) -> "Self":
        self.properties["attributes"] = list(values)
        return self
    
    def add_attribute(self, value: EntityAttribute) -> "Self":
        self.properties.setdefault("attributes", []).append(value)
        return self
    
    def with_can_pick_up_loot(self, value: bool) -> "Self":
        self.properties["CanPickUpLoot"] = value
        return self
    
    def with_current_explosion_impact_pos(self, value: Position3 | tuple[float, float, float] | list[float]) -> "Self":
        self.properties["CurrentExplosionImpactPos"] = Position3.auto(value)
        return self
    
    def with_death_loot_table(self, value: str | Identifier | Holder[Identifier] | LootTable) -> "Self":
        if isinstance(value, LootTable):
            self.properties["DeathLootTable"] = value.id
        else:
            self.properties["DeathLootTable"] = IdentifierConverter.auto(value)
        return self
    
    def with_death_loot_table_seed(self, value: int) -> "Self":
        self.properties["DeathLootTableSeed"] = value
        return self
    
    def with_death_time(self, value: int) -> "Self":
        self.properties["DeathTime"] = value
        return self

    _TMobDropSlot = Literal[
        "head", "chest", "legs", "feet", "mainhand", "offhand", "body", "saddle"
    ]
    def with_drop_chances(
        self,
        value: dict[_TMobDropSlot, float]
    ) -> "Self":
        self.properties["drop_chances"] = value
        return self
    
    def with_equipment(
        self,
        value: dict[_TMobDropSlot, ItemStack]
    ) -> "Self":
        self.properties["equipment"] = value
        return self
    
    def with_fall_flying(self, value: byte) -> "Self":
        self.properties["FallFlying"] = value
        return self

    def with_health(self, value: float) -> "Self":
        self.properties["Health"] = value
        return self
    
    def with_hurt_time(self, value: short) -> "Self":
        self.properties["HurtTime"] = value
        return self
    
    def with_leash(self, value: tuple4[int] | list[int] | UUID) -> "Self":
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Leash"] = value
        return self
    
    def with_no_ai(self, value: bool) -> "Self":
        self.properties["NoAI"] = value
        return self
    
    def with_persistent(self, value: bool) -> "Self":
        self.properties["PersistenceRequired"] = value
        return self
    
    def with_team(self, value: EntityTeam | str) -> "Self":
        if isinstance(value, EntityTeam):
            self.properties["Team"] = value
        else:
            self.properties["Team"] = EntityTeam(value)
        return self