from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datagen.utils.repr.status_effect import StatusEffect

class AppliedStatusEffect():
    def __init__(self, effect: StatusEffect, duration: int | None = None, amplifier: int | None = None) -> None:
        self.effect = effect
        self.duration = duration
        self.amplifier = amplifier

    def to_dict(self) -> dict:
        data = {}
        data["effect"] = str(self.effect.id)
        if self.duration is not None:
            data["duration"] = self.duration
        if self.amplifier is not None:
            data["amplifier"] = self.amplifier
        return data