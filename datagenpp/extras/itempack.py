from typing import Any, Iterable, Type

from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.give import Give
from datagen.function.commands.summon import Summon
from datagen.utils.converters import Dictionary
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.position3 import Position3


class ItemPack():
    PACK_CUSTOM_DATA = {"pack": True}
    def __init__(self, items: Iterable[ItemStack[Item[Any]]]) -> None:
        self.items = list(items)

    def give(self, target: TargetSelector = TargetSelector.SELF) -> CommandArray:
        return CommandArray([Give(target, item) for item in self.items])
    
    def summon(self, at: Position3 = RelativePlayerPosition(0, 0, 0)) -> CommandArray:
        return CommandArray([Summon.item(item, at) for item in self.items])
    
    def bundle(self, settings: Item.Settings | dict = {}) -> Item:
        ITEMS = []
        for item in self.items:
            ITEMS.append(item.to_dict())
        return Item(
            Items.BUNDLE.id, 
            {
                "bundle_contents": ITEMS, 
                "custom_data": self.PACK_CUSTOM_DATA
            } | Dictionary[str, Any].auto(settings)
        )

        