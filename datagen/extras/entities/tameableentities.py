from typing import Self
from uuid import UUID

from datagen.extras.entities._util.hasproperties import HasProperties
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.repr.entitytype import EntityType

type tuple4[T] = tuple[T, T, T, T]

class TameableEntities[T: HasProperties]:
    def with_owner(self: T, value: tuple4[int] | list[int] | UUID) -> T:
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Owner"] = value
        return self
    
    def with_sitting(self: T, value: bool) -> T:
        self.properties["Sitting"] = value
        return self