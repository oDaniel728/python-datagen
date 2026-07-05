from typing import Literal, Self

from datagen.extras.entities.mobentity import MobEntity
from datagen.extras.repr.entity import Entity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class DisplayEntity(MobEntity):
    def __init__(self, type: EntityType):
        super().__init__(type)
        
    _TBillboardType = Literal["fixed", "horizontal", "vertical", "center"]
    def with_billboard(self, value: _TBillboardType = "fixed") -> "Self":
        self.properties["billboard"] = value
        return self

    _TBrightnessLevel = int | Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
    def with_brightness(self, block: _TBrightnessLevel, sky: _TBrightnessLevel) -> "Self":
        self.properties["brightness"] = {"block": int(block), "sky": int(sky)}
        return self
    
    def with_glow_color_override(self, value: int) -> "Self":
        self.properties["glow_color_override"] = value
        return self

    def with_width(self, value: float) -> "Self":
        self.properties["width"] = value
        return self
    
    def with_height(self, value: float) -> "Self":
        self.properties["height"] = value
        return self
    
    def with_interpolation_duration(self, value: int) -> "Self":
        self.properties["interpolation_duration"] = value
        return self
    
    def with_teleport_duration(self, value: int) -> "Self":
        self.properties["teleport_duration"] = value
        return self
    
    def with_start_interpolation(self, value: bool) -> "Self":
        self.properties["start_interpolation"] = value
        return self
    
    def with_shadow_radius(self, value: float) -> "Self":
        self.properties["shadow_radius"] = value
        return self
    
    def with_shadow_strength(self, value: float) -> "Self":
        self.properties["shadow_strength"] = value
        return self
    
    def with_view_range(self, value: float) -> "Self":
        self.properties["view_range"] = value
        return self
    
    def with_transformation_right_rotation(self, angle: float, axis: tuple[float, float, float] | list[float]) -> "Self":
        self.properties.setdefault("transformation", {})["right_rotation"] = {"angle": angle, "axis": list(axis)}
        return self

    def with_transformation_left_rotation(self, angle: float, axis: tuple[float, float, float] | list[float]) -> "Self":
        self.properties.setdefault("transformation", {})["left_rotation"] = {"angle": angle, "axis": list(axis)}
        return self
    
    def with_scale(self, value: tuple[float, float, float] | list[float]) -> "Self":
        self.properties.setdefault("transformation", {})["scale"] = list(value)
        return self
    
    def with_translation(self, value: tuple[float, float, float] | list[float]) -> "Self":
        self.properties.setdefault("transformation", {})["translation"] = list(value)
        return self