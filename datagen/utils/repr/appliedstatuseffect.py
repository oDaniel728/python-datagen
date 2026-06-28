from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datagen.utils.repr.status_effect import StatusEffect

class AppliedStatusEffect():
    def __init__(self, effect: StatusEffect, duration: int | None = None, amplifier: int | None = None) -> None:
        self.effect = effect
        self.duration = duration
        self.amplifier = amplifier
        self.ambient: bool | None = None
        self.show_particles: bool | None = None
        self.show_icon: bool | None = None

    def to_dict(self) -> dict:
        data = {}
        data["id"] = str(self.effect.id)
        if self.duration is not None:
            data["duration"] = self.duration
        if self.amplifier is not None:
            data["amplifier"] = self.amplifier
        if self.ambient is not None:
            data["ambient"] = self.ambient
        if self.show_particles is not None:
            data["show_particles"] = self.show_particles
        if self.show_icon is not None:
            data["show_icon"] = self.show_icon
        return data