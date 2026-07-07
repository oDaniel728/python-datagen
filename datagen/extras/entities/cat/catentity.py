from typing import Literal

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.extras.entities.tameableentities import TameableEntities
from datagen.extras.utils.color_dyes import ColorDyes
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.entitytype import EntityType


class CatEntity(BaseEntity, MobEntity, TameableEntities):
    def __init__(self):
        super().__init__(EntityTypes.CAT)

    def with_collar_color(self, color: ColorDyes._TColorDyes | int) -> "CatEntity":
        if isinstance(color, str):
            self.properties["collar_color"] = ColorDyes.get_dye_color(color)
        else:
            self.properties["collar_color"] = color
        return self
    
    VARIANT_WHITE = Identifier.of("minecraft", "white")
    VARIANT_TUXEDO = Identifier.of("minecraft", "tuxedo")
    VARIANT_GINGER = Identifier.of("minecraft", "ginger")
    VARIANT_SIAMESE = Identifier.of("minecraft", "siamese")
    VARIANT_BRITISH_SHORTHAIR = Identifier.of("minecraft", "british_shorthair")
    VARIANT_CALICO = Identifier.of("minecraft", "calico")
    VARIANT_PERSIAN = Identifier.of("minecraft", "persian")
    VARIANT_RAGDOLL = Identifier.of("minecraft", "ragdoll")
    VARIANT_TABBY = Identifier.of("minecraft", "tabby")
    VARIANT_BLACK = Identifier.of("minecraft", "black")
    VARIANT_JELLIE = Identifier.of("minecraft", "jellie")

    def with_variant(self, variant: Identifier) -> "CatEntity":
        self.properties["variant"] = variant
        return self