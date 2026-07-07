from typing import Self

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class EndermiteEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ENDERMITE)

    def with_lifetime(self, lifetime: int) -> "Self":
        """
        The lifetime of the endermite in ticks.
        The endermite will despawn when this reaches 0.
        """
        self.properties["Lifetime"] = lifetime
        return self