from uuid import UUID

from datagen.extras.entities._util.hasproperties import HasProperties

type tuple4[T] = tuple[T, T, T, T]

class OwnableEntities[T: HasProperties]:
    def with_owner(self: T, value: tuple4[int] | list[int] | UUID) -> T:
        if isinstance(value, (tuple, list)):
            value = UUID(bytes=bytes(value))
        self.properties["Owner"] = value
        return self