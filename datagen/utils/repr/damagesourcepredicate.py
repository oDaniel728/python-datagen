from datagen.types.util.validpredicate import ValidPredicate
from datagen.utils.repr.entitypredicate import EntityPredicate


class DamageSourcePredicate(ValidPredicate):
    def __init__(self) -> None:
        self._data: dict = {}

    def with_source_entity(self, entity: EntityPredicate) -> "DamageSourcePredicate":
        self._data["source_entity"] = entity.to_dict()
        return self

    def with_direct_entity(self, entity: EntityPredicate) -> "DamageSourcePredicate":
        self._data["direct_entity"] = entity.to_dict()
        return self

    def with_tag(self, tag: str, expected: bool = True) -> "DamageSourcePredicate":
        tags = self._data.setdefault("tags", [])
        tags.append({"id": tag, "expected": expected})
        return self

    def with_is_direct(self, value: bool) -> "DamageSourcePredicate":
        self._data["is_direct"] = value
        return self

    def set(self, key: str, value) -> "DamageSourcePredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
