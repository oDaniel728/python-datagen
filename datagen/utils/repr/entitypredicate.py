from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.locationpredicate import LocationPredicate


class EntityPredicate():
    def __init__(self) -> None:
        self._data: dict = {}

    def with_type(self, entity_type: EntityType) -> "EntityPredicate":
        self._data["type"] = str(entity_type)
        return self

    def with_location(self, location: LocationPredicate) -> "EntityPredicate":
        self._data["location"] = location.to_dict()
        return self

    def with_stepping_on(self, location: LocationPredicate) -> "EntityPredicate":
        self._data["stepping_on"] = location.to_dict()
        return self

    def with_equipment(self, slot: str, item: ItemPredicate) -> "EntityPredicate":
        equipment = self._data.setdefault("equipment", {})
        equipment[slot] = item.to_dict()
        return self

    def with_nbt(self, nbt: str) -> "EntityPredicate":
        self._data["nbt"] = nbt
        return self

    def set(self, key: str, value) -> "EntityPredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
