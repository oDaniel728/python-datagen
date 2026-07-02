from typing import Literal, TypedDict

from datagen.utils._dictify import dictify
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.appliedstatuseffect import AppliedStatusEffect
from datagen.utils.repr.enchantment import Enchantment
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.extras.item.settings.toolrule import ToolRule


class BaseItemSettings(Item.Settings):
    def __init__(self):
        super().__init__()
        self._data = {}

    def with_(self, key: str, value: str):
        self._data[key] = value
        return self

    def with_enchantment_glint_override(self, override: bool):
        self._data["enchantment_glint_override"] = override
        return self

    def with_enchantments(self, enchantments: dict[Enchantment, int], show_in_tooltip: bool = True):
        self._data["enchantments"] = {
            "enchantments": {enchantment.id.to_string(): level for enchantment, level in enchantments.items()},
            "show_in_tooltip": show_in_tooltip
        }
        return self

    def with_custom_data(self, data: dict):
        from datagen.utils.obfuscator import Obfuscator
        from datagen.utils.snbtserializer import SNBTSerializer
        data = {
            Obfuscator.obfuscate(key, "other.item_custom_data_keys") if isinstance(key, str) else key: value
            for key, value in data.items()
        }
        self._data["custom_data"] = SNBTSerializer.serialize(data)
        return self
    
    def with_hide_tooltip(self):
        self._data["hide_tooltip"] = {}
        return self
    
    class _TEffect(TypedDict):
        effect: AppliedStatusEffect
        probability: float

    def with_food(
        self,
        nutrition: int = 0,
        saturation: float = 0.0,
        can_always_eat: bool = True,
        eat_seconds: float = 0.05,
        effects: list[_TEffect] | None = None,
        using_converts_to: ItemStack | None = None
    ):
        self._data["food"] = {
            "nutrition": nutrition,
            "saturation": saturation,
            "can_always_eat": can_always_eat,
            "eat_seconds": eat_seconds,
            "effects": [
                {
                    "effect": effect["effect"].to_dict(),
                    "probability": effect["probability"]
                } for effect in effects
            ] if effects else [],
            "using_converts_to": using_converts_to.to_dict() if using_converts_to else None
        }
        return self

    def with_item_name(
        self,
        name: Text.BaseText
    ):
        self._data["item_name"] = name.to_string()
        return self
    
    def with_fire_resistant(self):
        self._data["fire_resistant"] = {}
        return self
    
    def with_jukebox_playable(
        self,
        sound: Identifier,
        show_in_tooltip: bool = True
    ):
        self._data["jukebox_playable"] = {
            "sound": str(sound),
            "show_in_tooltip": show_in_tooltip
        }
        return self
    
    def with_lore(
        self,
        lore: list[Text.BaseText]
    ):
        self._data["lore"] = [text.to_string() for text in lore]
        return self
    
    def with_max_stack_size(self, size: int):
        self._data["max_stack_size"] = size
        return self
    
    _TRarity = Literal["common", "uncommon", "rare", "epic"]
    def with_rarity(self, rarity: _TRarity):
        self._data["rarity"] = rarity
        return self
    
    def with_repair_cost(self, cost: int):
        self._data["repair_cost"] = cost
        return self
    
    def with_tool(self, tool_rule: ToolRule):
        self._data["tool"] = tool_rule.to_dict()
        return self
    
    def with_max_damage(self, max_damage: int):
        self._data["max_damage"] = max_damage
        self.with_max_stack_size(1)
        return self
    
    def with_damage(self, damage: int):
        self._data["damage"] = damage
        self.with_max_stack_size(1)
        return self

    def with_unbreakable(self):
        self._data["unbreakable"] = {}
        self.with_max_stack_size(1)
        return self

    def get_components(self) -> dict:
        return dictify(self._data)