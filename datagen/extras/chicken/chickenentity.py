from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class ChickenEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.CHICKEN)

    def with_egg_lay_time(self, egg_lay_time: int) -> "ChickenEntity":
        """
        Number of ticks until the chicken lays its egg.
        Laying occurs at 0 and this timer gets reset to a new random value between 6000 and 12000.
        """
        self.properties["EggLayTime"] = egg_lay_time
        return self

    def with_is_chicken_jockey(self, is_chicken_jockey: bool) -> "ChickenEntity":
        """
        Whether or not the chicken is a jockey for a baby zombie.
        If true, the chicken can naturally despawn, drops 10 experience upon death
        instead of 1-3 and cannot lay eggs.
        """
        self.properties["IsChickenJockey"] = is_chicken_jockey
        return self