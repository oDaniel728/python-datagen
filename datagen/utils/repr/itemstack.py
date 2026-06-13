
from datagen.utils.repr.item import Item


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
        return f"{Item.__str__(self.item)} {self.count}"