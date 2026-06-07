from typing import overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3
from datagen.utils.repr.sound import Sound
from datagen.utils.repr.soundsource import SoundSource


class PlaySound(Command):
    @overload
    def __init__(self, 
        sound: Sound, 
        source: SoundSource, 
        target: TargetSelector, 
        at: Position3, 
        volume: float, 
        pitch: float, 
        min_volume: float, 
        /
    ) -> None: ...
    @overload
    def __init__(self, 
        sound: Sound, 
        source: SoundSource, 
        target: TargetSelector, 
        at: Position3, 
        volume: float, 
        /
    ) -> None: ...
    @overload
    def __init__(self, 
        sound: Sound, 
        source: SoundSource, 
        target: TargetSelector, 
        at: Position3, 
        /
    ) -> None: ...
    @overload
    def __init__(self, 
        sound: Sound, 
        source: SoundSource, 
        target: TargetSelector, 
        /
    ) -> None: ...

    def __init__(self, 
        sound: Sound, 
        source: SoundSource, 
        target: TargetSelector, 
        at: Position3 | None = None, 
        volume: float | None = None, 
        pitch: float | None = None, 
        min_volume: float | None = None, 
        /
    ) -> None:
        super().__init__()

        self.sound = sound
        self.source = source
        self.target = target
        self.at = at
        self.volume = volume
        self.pitch = pitch
        self.min_volume = min_volume

    def to_string(self) -> str:
        return f"playsound {self.sound} {self.source} {self.target}" + \
            (f" {self.at}" if self.at is not None else "") + \
            (f" {self.volume}" if self.volume is not None else "") + \
            (f" {self.pitch}" if self.pitch is not None else "") + \
            (f" {self.min_volume}" if self.min_volume is not None else "")