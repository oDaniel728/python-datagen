from typing import Literal, Self

from datagen.extras.color import Color
from datagen.extras.entities.display.displayentity import DisplayEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.text._base import BaseText
from datagen.types.util.reprs import byte


class TextDisplayEntity(DisplayEntity):
    def __init__(self):
        super().__init__(EntityTypes.TEXT_DISPLAY)

    _TAligntment = Literal["left", "center", "right"]
    def with_alignment(self, value: _TAligntment = "center") -> "Self":
        self.properties["alignment"] = value
        return self
    
    def with_background(self, value: Color) -> "Self":
        self.properties["background"] = value.to_hex()
        return self
    
    def with_default_background(self, value: bool = False) -> "Self":
        self.properties["default_background"] = value
        return self

    def with_line_width(self, value: float) -> "Self":
        self.properties["line_width"] = value
        return self
    
    def with_see__through(self, value: bool = False) -> "Self":
        self.properties["see_through"] = value
        return self
    
    def with_shadow(self, value: bool = False) -> "Self":
        self.properties["shadow"] = value
        return self

    def with_text(self, value: BaseText | list[BaseText]) -> "Self":
        if isinstance(value, BaseText):
            return self.with_text([value])
        else:
            self.properties["text"] = str([v.to_dict() for v in value])
        return self
    
    def with_text_opacity(self, value: byte = -1) -> "Self":
        self.properties["text_opacity"] = int(value)
        return self
    
