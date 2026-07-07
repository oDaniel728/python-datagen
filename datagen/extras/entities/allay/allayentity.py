from datagen.extras.entities.allay.allaylistener import AllayListener
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.itemstack import ItemStack


class AllayEntity(MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ALLAY)

    def with_duplication_cooldown(self, duplication_cooldown: int) -> "AllayEntity":
        self.properties["DuplicationCooldown"] = duplication_cooldown
        return self

    def with_inventory(self, value: list[ItemStack]) -> "AllayEntity":
        self.properties["Inventory"] = value
        return self
    
    def with_listener(self, listener: "AllayListener") -> "AllayEntity":
        self.properties["Listener"] = listener
        return self