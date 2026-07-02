from typing import Any

from datagen.loot_table.loot_table import LootTable
from datagen.utils.minecraft.collections.attributes import Attributes
from datagen.utils.minecraft.collections.status_effects import StatusEffects
from datagen.utils.repr.attribute import Attribute
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.status_effect import StatusEffect
from datagen.extras.repr.entity import Entity


class Coin(Entity):
    def __init__(self, et: EntityType, loot_table: LootTable, health: int = 10, max_health: int = -1, **kwargs: Any) -> None:
        super().__init__(
            et, 
            {
                "NoAI": True, 
                "NoGravity": True, 
                "Health": health, 
                "Tags": ["coin"],
                # "Silent": True, 
                "DeathLootTable": loot_table.id,
                "attributes": [
                    {
                        "id": Attributes.GENERIC_MAX_HEALTH.get(),
                        "base": (max_health if max_health >= 0 else health)
                    }
                ],
                **kwargs
            }
        )