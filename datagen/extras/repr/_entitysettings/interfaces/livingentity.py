from datagen.extras.repr._entitysettings.interfaces.ageingentity import AgeingEntity
from datagen.extras.repr._entitysettings.interfaces.healthyentity import HealthyEntity


class LivingEntity(HealthyEntity, AgeingEntity):
    def __init__(self) -> None:
        super().__init__()