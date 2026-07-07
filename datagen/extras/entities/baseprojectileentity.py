from typing import Self
from uuid import UUID

from datagen.extras.entities.baseentity import BaseEntity
from datagen.utils.repr.entitytype import EntityType
from datagen.types.util.reprs import *

class BaseProjectileEntity(BaseEntity):
    def __init__(self, type: EntityType):
        super().__init__(type)

    def with_has_been_shot(self, value: bool) -> "Self":
        self.properties["HasBeenShot"] = value
        return self
    
    def with_left_owner(self, value: bool) -> "Self":
        self.properties["LeftOwner"] = value
        return self
    
    def with_owner(self, value: tuple4[int] | list[int] | UUID) -> "Self":
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Owner"] = value
        return self