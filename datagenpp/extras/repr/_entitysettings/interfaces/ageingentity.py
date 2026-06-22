from typing import Self

from datagenpp.extras.repr.entitysettings import EntitySettings


class AgeingEntity(EntitySettings):
    def __init__(self) -> None:
        super().__init__()

    def with_age(self, age: int) -> "Self":
        self.nbt["Age"] = age
        return self