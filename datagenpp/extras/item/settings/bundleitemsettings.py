from typing import Iterable, Self

from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack

class BundleItemSettings(Item.Settings):
    def __init__(self) -> None:
        super().__init__()

    def with_bundle_contents(self, contents: Iterable[ItemStack | Item]) -> "Self":
        self._bundle_contents = []
        for i in contents:
            if isinstance(i, Item):
                self._bundle_contents.append(i.get_stack(1))
            elif isinstance(i, ItemStack):
                self._bundle_contents.append(i)
            else:
                raise TypeError(f"Expected Item or ItemStack, got {type(i).__name__}")
        return self
    
    def get_components(self) -> dict:
        return {
            "bundle_contents": [i.to_dict() for i in self._bundle_contents]
        }