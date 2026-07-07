from typing import Self
from uuid import UUID

from datagen.entityteam import EntityTeam
from datagen.extras.entities._util.hasproperties import HasProperties
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


class MobEntity[T: HasProperties]:
    def with_absorption_amount(self: T, value: float) -> T:
        self.properties["AbsorptionAmount"] = value
        return self
    
    def with_active_effects(self: T, values: list[AppliedStatusEffect]) -> T:
        self.properties["ActiveEffects"] = list(values)
        return self
    
    def add_active_effect(self: T, value: AppliedStatusEffect) -> T:
        self.properties.setdefault("ActiveEffects", []).append(value)
        return self
    
    def with_attributes(self: T, values: list[EntityAttribute]) -> T:
        self.properties["attributes"] = list(values)
        return self
    
    def add_attribute(self: T, value: EntityAttribute) -> T:
        self.properties.setdefault("attributes", []).append(value)
        return self
    
    def with_can_pick_up_loot(self: T, value: bool) -> T:
        self.properties["CanPickUpLoot"] = value
        return self
    
    def with_current_explosion_impact_pos(self: T, value: Position3 | tuple[float, float, float] | list[float]) -> T:
        self.properties["CurrentExplosionImpactPos"] = Position3.auto(value)
        return self
    
    def with_death_loot_table(self: T, value: str | Identifier | Holder[Identifier] | LootTable) -> T:
        if isinstance(value, LootTable):
            self.properties["DeathLootTable"] = value.id
        else:
            self.properties["DeathLootTable"] = IdentifierConverter.auto(value)
        return self
    
    def with_death_loot_table_seed(self: T, value: int) -> T:
        self.properties["DeathLootTableSeed"] = value
        return self
    
    def with_death_time(self: T, value: int) -> T:
        self.properties["DeathTime"] = value
        return self

    _TMobDropSlot = Literal[
        "head", "chest", "legs", "feet", "mainhand", "offhand", "body", "saddle"
    ]
    def with_drop_chances(
        self: T,
        value: dict[_TMobDropSlot, float]
    ) -> T:
        self.properties["drop_chances"] = value
        return self
    
    def with_equipment(
        self: T,
        value: dict[_TMobDropSlot, ItemStack]
    ) -> T:
        self.properties["equipment"] = value
        return self
    
    def with_fall_flying(self: T, value: byte) -> T:
        self.properties["FallFlying"] = value
        return self

    def with_health(self: T, value: float) -> T:
        self.properties["Health"] = value
        return self
    
    def with_hurt_time(self: T, value: short) -> T:
        self.properties["HurtTime"] = value
        return self
    
    def with_leash(self: T, value: tuple4[int] | list[int] | UUID) -> T:
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Leash"] = value
        return self
    
    def with_no_ai(self: T, value: bool) -> T:
        self.properties["NoAI"] = value
        return self
    
    def with_persistent(self: T, value: bool) -> T:
        self.properties["PersistenceRequired"] = value
        return self
    
    def with_team(self: T, value: EntityTeam | str) -> T:
        if isinstance(value, EntityTeam):
            self.properties["Team"] = value
        else:
            self.properties["Team"] = EntityTeam(value)
        return self