from typing import Self

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._base import BaseText, _remove_nulls
from datagen.utils.simplefile import SimpleFile


class EnchantmentProvider(ToDict):
    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.get(id)
        self._data: dict = {}

    # --- Basic properties ---

    def with_description(self, description: str | BaseText) -> Self:
        if isinstance(description, BaseText):
            self._data["description"] = _remove_nulls(description.to_dict())
        else:
            self._data["description"] = description
        return self

    def with_exclusive_set(self, *enchantments: str | Identifier) -> Self:
        self._data["exclusive_set"] = [str(e) for e in enchantments]
        return self

    def with_supported_items(self, *items: str | Identifier) -> Self:
        self._data["supported_items"] = [str(i) for i in items]
        return self

    def with_primary_items(self, *items: str | Identifier) -> Self:
        self._data["primary_items"] = [str(i) for i in items]
        return self

    def with_weight(self, weight: int) -> Self:
        self._data["weight"] = weight
        return self

    def with_max_level(self, level: int) -> Self:
        self._data["max_level"] = level
        return self

    def with_cost(self, min_base: int, min_per_level: int, max_base: int, max_per_level: int) -> Self:
        self._data["min_cost"] = {"base": min_base, "per_level_above_first": min_per_level}
        self._data["max_cost"] = {"base": max_base, "per_level_above_first": max_per_level}
        return self

    def with_anvil_cost(self, cost: int) -> Self:
        self._data["anvil_cost"] = cost
        return self

    def with_slots(self, *slots: str) -> Self:
        self._data["slots"] = list(slots)
        return self

    # --- Effects ---

    def with_effect(self, component_id: str, *entries: dict) -> Self:
        if "effects" not in self._data:
            self._data["effects"] = {}
        if component_id not in self._data["effects"]:
            self._data["effects"][component_id] = []
        self._data["effects"][component_id].extend(entries)
        return self

    def with_value_effect(self, component_id: str, effect: ToDict, requirements: dict | None = None, enchanted: str | None = None) -> Self:
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        return self.with_effect(component_id, EffectComponent.value_component(effect, requirements, enchanted))

    def with_entity_effect(self, component_id: str, effect: ToDict, enchanted: str, affected: str, requirements: dict | None = None) -> Self:
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        return self.with_effect(component_id, EffectComponent.entity_component(effect, enchanted, affected, requirements))

    def with_attributes(self, *attributes: ToDict) -> Self:
        self._data["effects"] = self._data.get("effects", {})
        if "minecraft:attributes" not in self._data["effects"]:
            self._data["effects"]["minecraft:attributes"] = []
        for attr in attributes:
            self._data["effects"]["minecraft:attributes"].append(_remove_nulls(attr.to_dict()) if hasattr(attr, "to_dict") else _remove_nulls(attr))
        return self

    def with_damage_immunity(self, requirements: dict | None = None) -> Self:
        entry: dict = {"effect": {}}
        if requirements is not None:
            entry["requirements"] = requirements
        return self.with_effect("minecraft:damage_immunity", _remove_nulls(entry))

    def with_prevent_equipment_drop(self) -> Self:
        return self.with_effect("minecraft:prevent_equipment_drop", {})

    def with_prevent_armor_change(self) -> Self:
        return self.with_effect("minecraft:prevent_armor_change", {})

    def with_location_changed(self, effect: ToDict, requirements: dict | None = None) -> Self:
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        entry: dict = {"effect": effect.to_dict() if hasattr(effect, "to_dict") else effect}
        if requirements is not None:
            entry["requirements"] = requirements
        return self.with_effect("minecraft:location_changed", entry)

    def with_crossbow_charge_sounds(self, *levels: dict) -> Self:
        return self.with_effect("minecraft:crossbow_charge_sounds", *levels)

    def with_trident_sound(self, *sounds: str) -> Self:
        return self.with_effect("minecraft:trident_sound", *[_remove_nulls(sound) for sound in sounds]) # type: ignore

    # --- Serialization ---

    def get_filepath(self) -> str:
        return f"enchantment/{self.id._path}.json"

    def to_dict(self) -> dict:
        return dict(self._data)

    def to_file(self) -> SimpleFile:
        import json
        return SimpleFile(self.get_filepath(), json.dumps(self.to_dict(), indent=4))

    # --- Auto-registration ---

    def __invert__(self) -> Self:
        self.namespace.add_enchantment(self)
        return self
