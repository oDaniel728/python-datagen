from typing import Self

from datagen.extras.repr.entitysettings import EntitySettings


class HealthyEntity(EntitySettings):
    def __init__(self) -> None:
        super().__init__()

    def with_health(self, health: float) -> "Self":
        self.nbt["Health"] = health
        return self