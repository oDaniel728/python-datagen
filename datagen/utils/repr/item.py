from typing import TYPE_CHECKING, Any, Self, overload

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
if TYPE_CHECKING:
    from datagen.utils.repr.itemstack import ItemStack

class Item[T: ToDict | dict[str, Any]]():
    def __init__(self, id: Identifier, components: T) -> None:
        self.id = id
        self.nbt = components

    def __get_nbt_dict(self) -> dict:
        if not isinstance(self.nbt, dict):
            return self.nbt.to_dict()
        return self.nbt

    def __str__(self) -> str:
        return f"{~self.id}[{','.join(f'\"{k}\"={v}' for k, v in self.__get_nbt_dict().items())}]"

    def __invert__(self):
        return self.id
    
    # utils
    @overload
    def to_item_stack(self) -> "ItemStack": ...
    @overload
    def to_item_stack(self, count: int = 1) -> "ItemStack": ...

    def to_item_stack(self, count: int = 1) -> "ItemStack":
        from datagen.utils.repr.itemstack import ItemStack
        return ItemStack(self, count)

    def copy(self) -> "Item[T]":
        return Item(self.id, self.nbt)