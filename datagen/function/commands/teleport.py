from typing import overload

from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
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
    def __init__(self, target: TargetSelector, destination: str, /) -> None: ...
    @overload
    def __init__(self, target: str, /) -> None: ...
    @overload
    def __init__(self, target: Position3, /) -> None: ...

    def __init__(self, *args) -> None:
        super().__init__()
        self.target: TargetSelector | Position3 | str
        self.destination: TargetSelector | Position3 | str
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
        target_str = self.target.to_string() if hasattr(self.target, "to_string") else str(self.target) # type: ignore
        destination_str = self.destination.to_string() if hasattr(self.destination, "to_string") else str(self.destination) # type: ignore
        return self.auto_macro(f"tp {target_str} {destination_str}")
    
    @staticmethod
    def look_at_entity(at: TargetSelector | str, /) -> Command:
        at_str = at.to_string() if hasattr(at, "to_string") else str(at) # type: ignore
        return CustomCommand(f"tp @s ~ ~ ~ facing entity {at_str}")
    
    @staticmethod
    def look_at_position(at: Position3 | str, /) -> Command:
        at_str = at.to_string() if hasattr(at, "to_string") else str(at) # type: ignore
        return CustomCommand(f"tp @s ~ ~ ~ facing {at_str}")