from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class LlamaEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.LLAMA)

    def with_bred(self, value: bool) -> "LlamaEntity":
        self.properties["Bred"] = value
        return self

    def with_eating_haystack(self, value: bool) -> "LlamaEntity":
        self.properties["EatingHaystack"] = value
        return self

    def with_owner(self, value: list[int]) -> "LlamaEntity":
        self.properties["Owner"] = value
        return self

    def with_tame(self, value: bool) -> "LlamaEntity":
        self.properties["Tame"] = value
        return self

    def with_temper(self, value: int) -> "LlamaEntity":
        self.properties["Temper"] = value
        return self

    def with_chested_horse(self, value: bool) -> "LlamaEntity":
        self.properties["ChestedHorse"] = value
        return self

    def with_despawn_delay(self, value: int) -> "LlamaEntity":
        self.properties["DespawnDelay"] = value
        return self

    def with_items(self, value: list[ItemStack]) -> "LlamaEntity":
        self.properties["Items"] = value
        return self

    def with_strength(self, value: int) -> "LlamaEntity":
        self.properties["Strength"] = value
        return self

    def with_variant(self, value: int) -> "LlamaEntity":
        self.properties["Variant"] = value
        return self