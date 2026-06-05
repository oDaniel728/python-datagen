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

    def with_enchantment(self, enchantment: Enchantment, level: Range | None = None) -> "ItemPredicate":
        enchantments = self._data.setdefault("enchantments", [])
        entry: dict = {"enchantment": str(enchantment)}
        if level is not None:
            entry["levels"] = {"min": level.start, "max": level.end}
        enchantments.append(entry)
        return self

    def with_stored_enchantment(self, enchantment: Enchantment, level: Range | None = None) -> "ItemPredicate":
        enchantments = self._data.setdefault("stored_enchantments", [])
        entry: dict = {"enchantment": str(enchantment)}
        if level is not None:
            entry["levels"] = {"min": level.start, "max": level.end}
        enchantments.append(entry)
        return self

    def set(self, key: str, value) -> "ItemPredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
