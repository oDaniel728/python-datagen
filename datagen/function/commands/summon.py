import json
from typing import overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.position3 import Position3


class Summon():
    @overload
    @staticmethod
    def entity(
        entity: EntityType, 
        pos: Position3, 
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def entity(
        entity: EntityType, 
        pos: Position3, 
        nbt: dict,
        /
    ) -> CustomCommand: ...
    @staticmethod
    def entity(
        entity: EntityType, 
        pos: Position3, 
        nbt: dict | None = None
    ) -> CustomCommand:
        return CustomCommand(f"summon {entity} {pos} {'' if nbt is None else json.dumps(nbt)}")
    
    @staticmethod
    def item(
        item: Item | ItemStack,
        pos: Position3,
        nbt: dict | None = None
    ) -> CustomCommand:
        # /summon minecraft:item ~ ~ ~ { Item: { id:"minecraft:acacia_boat", count: 1, components: {} } }
        if isinstance(item, Item):
            item = ItemStack(item, 1)
        _nbt = {
            "Item": {
                "id": item.item.id,
                "count": item.count,
                "components": item.item.nbt if item.item.nbt is not None else {}
            }
        }
        return CustomCommand(f"summon item {pos} {'' if nbt is None else json.dumps(_nbt)}")