
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item
from datagen.utils.repr.position3 import Position3


class ItemStack[I: Item = Item]():
    def __init__(self, item: I, count: int):
        self.item = item
        self.count = count

    def to_dict(self) -> dict:
        return {
            "id": ~self.item.id,
            "components": self.item.__get_nbt_dict(),
            "count": self.count
        }
    
    def __str__(self) -> str:
        return f"{self.item} {self.count}"