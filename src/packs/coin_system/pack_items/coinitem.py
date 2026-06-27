from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item


class CoinItem(Item):
    def __init__(self, id: Identifier, lore: str, value: int) -> None:
        _lore = []
        _lore.append({"text": lore})
        _lore.append([{"italic": False, "text": "Value: ", "color": "white"}, {"italic": False, "text": str(value), "color": "gold"}])
        _lore = list(map(lambda x: str(x).replace("'", '"'), _lore))
        super().__init__(id, {"max_stack_size": 10, "lore": _lore})