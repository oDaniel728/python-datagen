from datagen.loot_table.loot_table import LootTable
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.repr.item import Item
from datagenpp.extras.repr.entity import Entity


class EntitySpawnEgg(Item):
    def __init__(self, entity: Entity) -> None:
        super().__init__(Items.IRON_GOLEM_SPAWN_EGG.id, {"entity_data": entity.nbt()})