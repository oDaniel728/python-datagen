from typing import overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.playerposition import PlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3


class Teleport(Command):

    @overload
    def __init__(self, target: TargetSelector, /) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, destination: TargetSelector, /) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, destination: Position3, /) -> None: ...
    @overload
    def __init__(self, target: Position3, /) -> None: ...

    def __init__(self, *args) -> None:
        super().__init__()
        self.target: TargetSelector | Position3
        self.destination: TargetSelector | Position3
        if len(args) == 2:
            t, d = args
            self.target = t
            self.destination = d
        elif len(args) == 1:
            t = args[0]
            self.target = TargetSelector.SELF
            self.destination = t
        else:
            raise Exception("Invalid arguments for Teleport command")

    def to_string(self) -> str:
        return self.auto_macro(f"tp {self.target.to_string()} {self.destination.to_string()}")