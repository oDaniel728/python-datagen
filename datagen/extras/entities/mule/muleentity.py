from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class MuleEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.MULE)

    def with_bred(self, value: bool) -> "MuleEntity":
        self.properties["Bred"] = value
        return self

    def with_eating_haystack(self, value: bool) -> "MuleEntity":
        self.properties["EatingHaystack"] = value
        return self

    def with_owner(self, value: list[int]) -> "MuleEntity":
        self.properties["Owner"] = value
        return self

    def with_tame(self, value: bool) -> "MuleEntity":
        self.properties["Tame"] = value
        return self

    def with_temper(self, value: int) -> "MuleEntity":
        self.properties["Temper"] = value
        return self

    def with_chested_horse(self, value: bool) -> "MuleEntity":
        self.properties["ChestedHorse"] = value
        return self

    def with_items(self, value: list[ItemStack]) -> "MuleEntity":
        self.properties["Items"] = value
        return self