from typing import Any

from datagen.loot_table.loot_table import LootTable
from datagen.utils.converters import Dictionary
from datagen.utils.repr.entitytype import EntityType
from datagenpp.extras.repr.entity import Entity


class Coin(Entity):
    def __init__(self, et: EntityType, loot_table: LootTable):
        super().__init__(
            et, 
            {
                "NoAI": True, 
                "NoGravity": True, 
                "Health": 12, 
                "Tags": ["coin"],
                "Silent": True, 
                "DeathLootTable": loot_table.id
            }
        )