from typing import Any

from datagen.types.util.min import Range
from datagen.utils.repr.enchantment import Enchantment
from datagen.utils.repr.item import Item


class ItemPredicate():
    def __init__(self) -> None:
        self._data: dict = {}

    def with_items(self, *items: Item) -> "ItemPredicate":
        self._data["items"] = [str(~item) for item in items]
        return self

    def with_count(self, count: Range) -> "ItemPredicate":
        self._data["count"] = {"min": count.start, "max": count.end}
        return self

    def with_components(self, components: dict[str, Any]) -> "ItemPredicate":
        self._data["components"] = components
        return self

    def set(self, key: str, value) -> "ItemPredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
