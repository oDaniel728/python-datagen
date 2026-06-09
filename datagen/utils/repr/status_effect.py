from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.appliedstatuseffect import AppliedStatusEffect


class StatusEffect():
    def __init__(self, id: Identifier) -> None:
        self.id = id

    def apply(self, duration: int | None = None, amplifier: int | None = None) -> "AppliedStatusEffect":
        return AppliedStatusEffect(self, duration, amplifier)