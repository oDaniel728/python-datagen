from datagen.extras.entities.angerentities import AngerEntities
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class BeeEntity(BreedableEntities, AngerEntities):
    def __init__(self):
        super().__init__(EntityTypes.BEE)

    def with_cannot_enter_hive_ticks(self, cannot_enter_hive_ticks: int):
        self.properties["CannotEnterHiveTicks"] = cannot_enter_hive_ticks
        return self
    
    def with_crops_grown_since_pollination(self, crops_grown_since_pollination: int):
        self.properties["CropsGrownSincePollination"] = crops_grown_since_pollination
        return self
    
    def with_flower_pos(self, flower_pos: tuple[int, int, int] | list[int] | BlockPosition):
        self.properties["FlowerPos"] = list(flower_pos)
        return self
    
    def with_has_nectar(self, has_nectar: bool):
        self.properties["HasNectar"] = has_nectar
        return self
    
    def with_has_stung(self, has_stung: bool):
        self.properties["HasStung"] = has_stung
        return self
    
    def with_hive_pos(self, hive_pos: tuple[int, int, int] | list[int] | BlockPosition):
        self.properties["hive_pos"] = list(hive_pos)
        return self
    
    def with_ticks_since_pollination(self, ticks_since_pollination: int):
        self.properties["TicksSincePollination"] = ticks_since_pollination
        return self