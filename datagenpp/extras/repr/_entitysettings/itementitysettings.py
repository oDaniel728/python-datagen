from datagen.utils.repr.itemstack import ItemStack
from datagenpp.extras.repr._entitysettings.interfaces.ageingentity import AgeingEntity
from datagenpp.extras.repr._entitysettings.interfaces.healthyentity import HealthyEntity
from datagen.types.util.reprs import *

class ItemEntitySettings(AgeingEntity, HealthyEntity):
    def __init__(self) -> None:
        super().__init__()

    def with_item(self, item: ItemStack):
        self.nbt["Item"] = item.to_dict()
        return self
    
    def with_owner(self, owner: tuple4[int]):
        owner = list(owner)
        self.nbt["Owner"] = f"[I; {owner[0]},{owner[1]},{owner[2]},{owner[3]}]"
        return self
    
    def with_pickup_delay(self, pickup_delay: int):
        self.nbt["PickupDelay"] = pickup_delay
        return self
    
    def with_thrower(self, thrower: tuple4[int]):
        thrower = list(thrower)
        self.nbt["Thrower"] = f"[I; {thrower[0]},{thrower[1]},{thrower[2]},{thrower[3]}]"
        return self