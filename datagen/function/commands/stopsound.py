from typing import Literal, overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.sound import Sound
from datagen.utils.repr.soundchannel import SoundChannel


class StopSound(Command):
    @overload
    def __init__(self, target: TargetSelector) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, source: SoundChannel | Literal["*"], sound: Sound) -> None: ...
    
    def __init__(self, target: TargetSelector, source: SoundChannel | Literal["*"] | None = None, sound: Sound | None = None):
        super().__init__()
        self.target = target
        self.source = source
        self.sound = sound

    def to_string(self) -> str:
        result = f"stopsound {self.target}"
        if self.source is not None:
            result += f" {self.source}"
            if self.sound is not None:
                result += f" {self.sound}"
        return result