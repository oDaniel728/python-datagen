
from datagen.utils.repr.item import Item


class ItemStack[I: Item = Item]():
    def __init__(self, item: I, count: int):
        self.item = item
        self.count = count

    def to_dict(self) -> dict:
        data = {}
        data['id'] = ~self.item.id
        data['count'] = self.count
        if c:=self.item.get_nbt_dict():
            data['components'] = c
        return data
    
    def __str__(self) -> str:
        return f"{Item.__str__(self.item)} {self.count}"
    
    def get_filter(self) -> str:
        return f"{self.item.get_item_filter()} {self.count}"
    
    def get_string(self) -> str:
        return f"{self.item.get_item_string()} {self.count}"