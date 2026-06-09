from datagen.utils.repr.entitytype import EntityType


class TypeSpecificPredicate:
    def __init__(self, type: EntityType):
        self.type = type
        self._data = {"type": ~type.id}

    def to_dict(self) -> dict:
        return self._data