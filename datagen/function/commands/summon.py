from datagen.utils.json_encoder import dumps
from typing import overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.position3 import Position3
from datagen.utils.snbtserializer import SNBTSerializer


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
        return CustomCommand(f"summon {entity} {pos} {'' if nbt is None else SNBTSerializer.serialize(nbt)}".strip())
    
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
                "components": item.item.settings if item.item.settings is not None else {}
            }
        }
        return CustomCommand(f"summon item {pos} {'' if nbt is None else dumps(_nbt)}")