from datagen.extras.repr._entitysettings.interfaces.ageingentity import AgeingEntity
from datagen.extras.repr._entitysettings.interfaces.healthyentity import HealthyEntity
from datagen.types.util.reprs import *

class ExperienceOrbEntitySettings(HealthyEntity, AgeingEntity):
    def __init__(self) -> None:
        super().__init__()

    def with_count(self, count: int):
        self.nbt["Count"] = count
        return self
    
    def with_value(self, value: short):
        self.nbt["Value"] = value
        return self