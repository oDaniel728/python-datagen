from typing import Self
from uuid import UUID

from datagen.extras.color import Color
from datagen.extras.entities.areaeffectcloud.potiontype import PotionType
from datagen.extras.entities.baseentity import BaseEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.appliedstatuseffect import AppliedStatusEffect
from datagen.types.util.reprs import *
from datagen.utils.repr.particle import ParticleType

class AreaEffectCloudEntity(BaseEntity):
    def __init__(self):
        super().__init__(EntityTypes.AREA_EFFECT_CLOUD)

    def with_age(self, age: int):
        "Age of the field. Increases by 1 every tick. When this is bigger than `Duration` + `WaitTime` the area effect cloud dissipates."
        self.properties["Age"] = age
        return self
    
    def with_duration(self, duration: int):
        "The maximum age of the field after `WaitTime`."
        self.properties["Duration"] = duration
        return self
    
    def with_duration_on_use(self, duration_on_use: int):
        "The amount the duration of the field changes upon applying the effect."
        self.properties["DurationOnUse"] = duration_on_use
        return self
    
    def with_potion_contents(self, potion: PotionType, custom_color: Color, custom_effects: list[AppliedStatusEffect]):
        "The potion and custom effects contained in this area effect cloud. Represents the `minecraft:potion_contents` component. If set to a string, it is converted to a compound, with the string corresponding to [String] potion. "
        self.properties["potion_contents"] = {
            "potion": potion,
            "custom_color": custom_color.to_int(),
            "custom_effects": [effect.to_dict() for effect in custom_effects]
        }
        return self
    
    def with_owner(self, value: tuple4[int] | list[int] | UUID) -> "Self":
        "The UUID of the entity who created the cloud, stored as four ints. Is not preserved when removed."
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Owner"] = value
        return self
    
    def with_particle(self, particle: ParticleType, **kwargs):
        "The particle displayed by the field."
        self.properties["Particle"] = {"type": particle, **kwargs}
        return self
    
    def with_radius(self, radius: float):
        "The field's radius."
        self.properties["Radius"] = radius
        return self
    
    def with_radius_on_use(self, radius_on_use: float):
        "The amount the radius changes upon applying the effect. Normally negative."
        self.properties["RadiusOnUse"] = radius_on_use
        return self
    
    def with_radius_per_tick(self, radius_per_tick: float):
        "The amount the radius changes per tick. Normally negative."
        self.properties["RadiusPerTick"] = radius_per_tick
        return self

    def with_reapplication_delay(self, reaplication_delay: int):
        "The number of ticks before reapplying the effect."
        self.properties["ReapplicationDelay"] = reaplication_delay
        return self
   
    def with_wait_time(self, wait_time: int):
        "The time before deploying the field. The `Radius` is ignored, meaning that any specified effects is not applied and specified particles appear only at the center of the field, until `Age` hits this number."
        self.properties["WaitTime"] = wait_time
        return self