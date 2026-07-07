from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class HorseEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.HORSE)

    def with_bred(self, value: bool) -> "HorseEntity":
        self.properties["Bred"] = value
        return self

    def with_eating_haystack(self, value: bool) -> "HorseEntity":
        self.properties["EatingHaystack"] = value
        return self

    def with_owner(self, value: list[int]) -> "HorseEntity":
        self.properties["Owner"] = value
        return self

    def with_tame(self, value: bool) -> "HorseEntity":
        self.properties["Tame"] = value
        return self

    def with_temper(self, value: int) -> "HorseEntity":
        self.properties["Temper"] = value
        return self

    def with_variant(self, value: int) -> "HorseEntity":
        self.properties["Variant"] = value
        return self

    def with_body_armor_item(self, value: ItemStack) -> "HorseEntity":
        self.properties["body_armor_item"] = value
        return self