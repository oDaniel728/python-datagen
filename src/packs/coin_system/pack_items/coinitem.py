from typing import Literal

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.minecraft.text._settings import LiteralTextSettings
from datagen.utils.repr.item import Item
from packs.coin_system.pack_settings.textsettings import BASIC, COMMON, EPIC, LEGENDARY, RARE, UNCOMMON


class CoinItem(Item):
    _TRarity = Literal["basic", "common", "uncommon", "rare", "epic", "legendary"]
    __RarityMap = dict[_TRarity, LiteralTextSettings]({
        "basic": BASIC,
        "common": COMMON,
        "uncommon": UNCOMMON,
        "rare": RARE,
        "epic": EPIC,
        "legendary": LEGENDARY
    })
    def __init__(self, id: Identifier, name: str, rarity: _TRarity, lore: str, value: int) -> None:
        _lore = []
        _lore.append({"text": lore})
        _lore.append([{"italic": False, "text": "Value: ", "color": "white"}, {"italic": False, "text": str(value), "color": "gold"}])
        _lore = list(map(lambda x: str(x).replace("'", '"'), _lore))
        super().__init__(id, {"max_stack_size": 99, "item_name": LiteralText(name, self.__RarityMap[rarity]), "lore": _lore, "custom_data": {"coin": True, "value": value, "show": True}})