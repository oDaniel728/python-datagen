from typing import Any, overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack


class Clear(Command):

    @overload
    def __init__(self, target: TargetSelector, /): ...
    @overload
    def __init__(self, target: TargetSelector, item: Item, /): ...
    @overload 
    def __init__(self, target: TargetSelector, stack: ItemStack, /): ...

    def __init__(self, *args):
        self.target: TargetSelector
        self.item: Item[Any] | ItemStack[Item[Any]] | None = None

        self.target, self.item = args

    def to_string(self) -> str:
        if self.item is None:
            return f"clear {self.target.to_string()}"
        else:
            if isinstance(self.item, ItemStack):
                return f"clear {self.target.to_string()} {self.item.item.__str__()} {self.item.count}"
            else:
                return f"clear {self.target.to_string()} {self.item.__str__()}"