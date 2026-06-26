import json
from pathlib import Path
from typing import Any

from datagen.globals import LOOT_TABLES_PATH
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.simplefile import SimpleFile


class _LootFunctions():

    @staticmethod
    def set_count(count: int | tuple[int, int] | list[int] | dict, add: bool = False) -> dict:
        return {
            "function": "minecraft:set_count",
            "count": {"min": count[0], "max": count[1]} if isinstance(count, tuple) else count,
            "add": add,
        }

    @staticmethod
    def set_damage(damage: float | tuple[float, float]) -> dict:
        return {
            "function": "minecraft:set_damage",
            "damage": {"min": damage[0], "max": damage[1]} if isinstance(damage, tuple) else damage,
        }

    @staticmethod
    def enchant_randomly(enchantments: list[str | Identifier] | None = None) -> dict:
        result: dict = {"function": "minecraft:enchant_randomly"}
        if enchantments:
            result["enchantments"] = [str(e) for e in enchantments]
        return result

    @staticmethod
    def enchant_with_levels(levels: int | tuple[int, int], treasure: bool = False) -> dict:
        return {
            "function": "minecraft:enchant_with_levels",
            "levels": {"min": levels[0], "max": levels[1]} if isinstance(levels, tuple) else levels,
            "treasure": treasure,
        }

    @staticmethod
    def set_attributes(attributes: list[dict]) -> dict:
        return {"function": "minecraft:set_attributes", "modifiers": attributes}

    @staticmethod
    def set_nbt(tag: str) -> dict:
        return {"function": "minecraft:set_nbt", "tag": tag}

    @staticmethod
    def set_name(name: str | dict) -> dict:
        return {"function": "minecraft:set_name", "name": name}

    @staticmethod
    def set_lore(lore: list[str | dict]) -> dict:
        return {"function": "minecraft:set_lore", "lore": lore}

    @staticmethod
    def set_stew_effect(effects: list[dict]) -> dict:
        return {"function": "minecraft:set_stew_effect", "effects": effects}

    @staticmethod
    def set_instrument(instrument: str | Identifier) -> dict:
        return {"function": "minecraft:set_instrument", "instrument": str(instrument)}

    @staticmethod
    def set_contents(entries: list[dict]) -> dict:
        return {"function": "minecraft:set_contents", "contents": entries}

    @staticmethod
    def set_fireworks(flight: int = 1, explosions: list[dict] | None = None) -> dict:
        result: dict = {"function": "minecraft:set_fireworks", "flight": flight}
        if explosions:
            result["explosions"] = explosions
        return result

    @staticmethod
    def set_book(attributes: dict) -> dict:
        result: dict = {"function": "minecraft:set_book"}
        result.update(attributes)
        return result

    @staticmethod
    def set_written_book_pages(pages: list[str | dict]) -> dict:
        return {"function": "minecraft:set_written_book_pages", "pages": pages}

    @staticmethod
    def furnace_smelt() -> dict:
        return {"function": "minecraft:furnace_smelt"}

    @staticmethod
    def copy_nbt(source: str, operations: list[dict]) -> dict:
        return {"function": "minecraft:copy_nbt", "source": source, "ops": operations}

    @staticmethod
    def copy_state(block: str | Identifier, properties: list[str]) -> dict:
        return {
            "function": "minecraft:copy_state",
            "block": str(block),
            "properties": properties,
        }

    @staticmethod
    def set_banner_pattern(patterns: list[dict]) -> dict:
        return {"function": "minecraft:set_banner_pattern", "patterns": patterns}

    @staticmethod
    def set_potion(potion: str | Identifier) -> dict:
        return {"function": "minecraft:set_potion", "id": str(potion)}

    @staticmethod
    def set_ominous_bottle(amplifier: int) -> dict:
        return {"function": "minecraft:set_ominous_bottle", "amplifier": amplifier}

    @staticmethod
    def explosion_decay() -> dict:
        return {"function": "minecraft:explosion_decay"}

    @staticmethod
    def limit_count(limit: dict | int) -> dict:
        return {"function": "minecraft:limit_count", "limit": limit}

    @staticmethod
    def apply_bonus(enchantment: str | Identifier, formula: str, parameters: dict) -> dict:
        return {
            "function": "minecraft:apply_bonus",
            "enchantment": str(enchantment),
            "formula": formula,
            "parameters": parameters,
        }


class _LootConditions():

    @staticmethod
    def random_chance(chance: float) -> dict:
        return {"condition": "minecraft:random_chance", "chance": chance}

    @staticmethod
    def random_chance_with_looting(chance: float, looting_multiplier: float = 0.0) -> dict:
        return {
            "condition": "minecraft:random_chance_with_looting",
            "chance": chance,
            "looting_multiplier": looting_multiplier,
        }

    @staticmethod
    def killed_by_player() -> dict:
        return {"condition": "minecraft:killed_by_player"}

    @staticmethod
    def killed_by_entity(predicate: dict | None = None) -> dict:
        result: dict = {"condition": "minecraft:killed_by_entity"}
        if predicate:
            result["entity_properties"] = predicate
        return result

    @staticmethod
    def entity_properties(entity: str, predicate: dict) -> dict:
        return {
            "condition": "minecraft:entity_properties",
            "entity": entity,
            "predicate": predicate,
        }

    @staticmethod
    def entity_scores(entity: str, scores: dict) -> dict:
        return {
            "condition": "minecraft:entity_scores",
            "entity": entity,
            "scores": scores,
        }

    @staticmethod
    def location_check(predicate: dict, offset_x: int = 0, offset_y: int = 0, offset_z: int = 0) -> dict:
        return {
            "condition": "minecraft:location_check",
            "predicate": predicate,
            "offsetX": offset_x,
            "offsetY": offset_y,
            "offsetZ": offset_z,
        }

    @staticmethod
    def weather_check(raining: bool | None = None, thundering: bool | None = None) -> dict:
        result: dict = {"condition": "minecraft:weather_check"}
        if raining is not None:
            result["raining"] = raining
        if thundering is not None:
            result["thundering"] = thundering
        return result

    @staticmethod
    def table_bonus(enchantment: str | Identifier, chances: list[float]) -> dict:
        return {
            "condition": "minecraft:table_bonus",
            "enchantment": str(enchantment),
            "chances": chances,
        }

    @staticmethod
    def time_check(value: int | dict, period: int | None = None) -> dict:
        result: dict = {
            "condition": "minecraft:time_check",
            "value": value if not isinstance(value, (tuple, list)) else {"min": value[0], "max": value[1]},
        }
        if period is not None:
            result["period"] = period
        return result

    @staticmethod
    def damage_source_properties(predicate: dict) -> dict:
        return {"condition": "minecraft:damage_source_properties", "predicate": predicate}

    @staticmethod
    def match_tool(predicate: dict) -> dict:
        return {"condition": "minecraft:match_tool", "predicate": predicate}

    @staticmethod
    def reference(id: str | Identifier) -> dict:
        return {"condition": "minecraft:reference", "name": str(id)}

    @staticmethod
    def survives_explosion() -> dict:
        return {"condition": "minecraft:survives_explosion"}

    @staticmethod
    def inverted(term: dict) -> dict:
        return {"condition": "minecraft:inverted", "term": term}

    @staticmethod
    def any_of(*terms: dict) -> dict:
        return {"condition": "minecraft:any_of", "terms": list(terms)}

    @staticmethod
    def all_of(*terms: dict) -> dict:
        return {"condition": "minecraft:all_of", "terms": list(terms)}

    @staticmethod
    def block_state_property(block: str | Identifier, properties: dict) -> dict:
        return {
            "condition": "minecraft:block_state_property",
            "block": str(block),
            "properties": properties,
        }

    @staticmethod
    def value_check(value: int | float | dict, range: dict) -> dict:
        return {
            "condition": "minecraft:value_check",
            "value": value if not isinstance(value, (tuple, list)) else {"min": value[0], "max": value[1]},
            "range": range,
        }


class _EntryBuilder():
    """Builder for a loot entry within a pool."""

    def __init__(self, pool_builder: "_PoolBuilder", entry_type: str, name: str | None = None) -> None:
        self.__pool_builder = pool_builder
        self.__data: dict = {"type": entry_type}
        if name is not None:
            self.__data["name"] = name
        self.__functions: list[dict] = []
        self.__conditions: list[dict] = []
        self.__children: list[dict] = []

    def weight(self, w: int) -> "_EntryBuilder":
        self.__data["weight"] = w
        return self

    def quality(self, q: int) -> "_EntryBuilder":
        self.__data["quality"] = q
        return self

    def function(self, func: dict) -> "_EntryBuilder":
        self.__functions.append(func)
        return self

    def condition(self, cond: dict) -> "_EntryBuilder":
        self.__conditions.append(cond)
        return self

    def child(self, entry_type: str = "minecraft:item", name: str | None = None) -> "_EntryBuilder":
        child_data: dict = {"type": entry_type}
        if name is not None:
            child_data["name"] = name
        self.__children.append(child_data)
        return self

    def then(self) -> "_PoolBuilder":
        """Finalizes this entry and returns to the pool builder for more entries."""
        if self.__functions:
            self.__data["functions"] = self.__functions
        if self.__conditions:
            self.__data["conditions"] = self.__conditions
        if self.__children:
            self.__data["children"] = self.__children
        self.__pool_builder.add_entry_data(self.__data)
        return self.__pool_builder


class _PoolBuilder():
    """Builder for a loot pool. Allows adding multiple entries."""

    def __init__(self, builder: "LootTableBuilder", rolls: int | dict | tuple[int, int], bonus_rolls: int | dict | tuple[int, int] | None = None) -> None:
        self.__builder = builder
        self.__rolls = rolls
        self.__bonus_rolls = bonus_rolls
        self.__entry_data: list[dict] = []
        self.__conditions: list[dict] = []
        self.__functions: list[dict] = []

    def add_entry_data(self, data: dict) -> None:
        self.__entry_data.append(data)

    def entry(self, entry_type: str = "minecraft:item", name: str | None = None) -> _EntryBuilder:
        return _EntryBuilder(self, entry_type, name)

    def condition(self, cond: dict) -> "_PoolBuilder":
        self.__conditions.append(cond)
        return self

    def function(self, func: dict) -> "_PoolBuilder":
        self.__functions.append(func)
        return self

    def end_pool(self) -> "LootTableBuilder":
        """Finalizes this pool and returns to the table builder."""
        pool_dict: dict = {
            "rolls": (
                {"min": self.__rolls[0], "max": self.__rolls[1]}
                if isinstance(self.__rolls, tuple)
                else self.__rolls
            ),
            "entries": self.__entry_data,
        }
        if self.__bonus_rolls is not None:
            pool_dict["bonus_rolls"] = (
                {"min": self.__bonus_rolls[0], "max": self.__bonus_rolls[1]}
                if isinstance(self.__bonus_rolls, tuple)
                else self.__bonus_rolls
            )
        if self.__conditions:
            pool_dict["conditions"] = self.__conditions
        if self.__functions:
            pool_dict["functions"] = self.__functions
        self.__builder.add_pool_data(pool_dict)
        return self.__builder


class LootTableBuilder():
    """Fluent builder for constructing loot tables.

    Examples:

        >>> LootTableBuilder(Identifier.of("mypack:chest")) \\
        ...     .pool(1).entry("minecraft:item", "minecraft:diamond").weight(1).then() \\
        ...     .end_pool() \\
        ...     .pool((2, 4)).entry("minecraft:item", "minecraft:iron_ingot").weight(3).then() \\
        ...     .end_pool() \\
        ...     .seal()
    """

    def __init__(self, id: Identifier) -> None:
        self.__id = id
        self.__pool_data: list[dict] = []
        self.__conditions: list[dict] = []
        self.__functions: list[dict] = []

    def pool(self, rolls: int | tuple[int, int] | dict, bonus_rolls: int | tuple[int, int] | dict | None = None) -> _PoolBuilder:
        return _PoolBuilder(self, rolls, bonus_rolls)

    def add_pool_data(self, data: dict) -> None:
        self.__pool_data.append(data)

    def condition(self, cond: dict) -> "LootTableBuilder":
        self.__conditions.append(cond)
        return self

    def function(self, func: dict) -> "LootTableBuilder":
        self.__functions.append(func)
        return self

    def seal(self) -> "LootTable":
        data: dict = {"type": "minecraft:loot_table", "pools": self.__pool_data}
        if self.__conditions:
            data["conditions"] = self.__conditions
        if self.__functions:
            data["functions"] = self.__functions
        return LootTable(self.__id, data)


class LootTable():
    """Represents a Minecraft loot table resource.

    Loot tables define what items are dropped from chests, entities, blocks,
    and other game mechanics. Each loot table has an identifier and contains
    pools of entries with associated conditions and functions.

    Examples:

        >>> lt = LootTable.builder(Identifier.of("mypack:simple")) \\
        ...     .pool(1).entry("minecraft:item", "minecraft:diamond").weight(1).then() \\
        ...     .end_pool() \\
        ...     .seal()
        >>> lt.to_string()
        '{\\n    "type": "minecraft:loot_table",\\n    "pools": [\\n        {\\n            "rolls": 1,\\n            "entries": [\\n                {\\n                    "type": "minecraft:item",\\n                    "name": "minecraft:diamond",\\n                    "weight": 1,\\n                    "functions": [],\\n                    "conditions": []\\n                }\\n            ]\\n        }\\n    ]\\n}'
    """

    __loot_tables: dict[Identifier, "LootTable"] = {}

    @staticmethod
    def builder(id: Identifier) -> LootTableBuilder:
        """Creates a new LootTableBuilder for the given identifier.

        Args:
            id: identifier for the loot table

        Examples:

            >>> lb = LootTable.builder(Identifier.of("mypack:chest"))
            >>> lt = lb.pool(1).entry("minecraft:item", "minecraft:diamond").weight(1).then().end_pool().seal()
        """
        return LootTableBuilder(id)

    def __new__(cls, id: Identifier, data: dict) -> "LootTable":
        if id in cls.__loot_tables:
            instance = cls.__loot_tables[id]
            instance._data = data
            return instance
        instance = super().__new__(cls)
        cls.__loot_tables[id] = instance
        return instance

    def __init__(self, id: Identifier, data: dict) -> None:
        from datagen.datapack.namespace import Namespace
        self._data = data
        self.id = id
        self.namespace = Namespace.temp()
        LootTable.__loot_tables[self.id] = self

    def __invert__(self) -> "LootTable":
        self.namespace.add_loot_table(self)
        return self

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LootTable):
            return self.id == other.id
        return NotImplemented

    def to_dict(self) -> dict:
        """Returns the loot table data as a plain dict."""
        _data = self._data.copy()
        if "type" not in _data:
            _data["type"] = "minecraft:loot_table"
        return _data

    def to_string(self) -> str:
        """Returns the loot table as a JSON string."""
        return json.dumps(self.to_dict(), indent=4)

    def get_filepath(self) -> Path:
        """Returns the relative file path for this loot table."""
        path = Obfuscator.obfuscate_path(self.id.get_namespace(), self.id.get_path())
        return Path(LOOT_TABLES_PATH) / (path.replace(".", "/") + ".json")

    def to_file(self) -> SimpleFile:
        """Returns a SimpleFile for writing to disk."""
        return SimpleFile(self.get_filepath(), self.to_string())
