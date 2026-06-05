from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.blockposition import BlockPosition


class Forceload():
    @overload
    @staticmethod
    def add(
        from_: BlockPosition,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def add(
        from_: BlockPosition,
        to: BlockPosition,
        /
    ) -> CustomCommand: ...
    @staticmethod
    def add(
        from_: BlockPosition,
        to: BlockPosition | None = None,
    ) -> CustomCommand:
        if to is not None:
            return CustomCommand(f"forceload add {from_} {to}")
        else:
            return CustomCommand(f"forceload add {from_}")
    
    @staticmethod
    def query(pos: BlockPosition, /) -> CustomCommand:
        return CustomCommand(f"forceload query {pos}")
    
    @overload
    @staticmethod
    def remove(
        from_: BlockPosition,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def remove(
        from_: BlockPosition,
        to: BlockPosition,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def remove(
        who: Literal["all"],
        /
    ) -> CustomCommand: ...
    @staticmethod
    def remove(
        from_: BlockPosition | Literal["all"],
        to: BlockPosition | None = None,
        /
    ) -> CustomCommand:
        if from_ == "all":
            return CustomCommand("forceload remove all")
        elif to is not None:
            return CustomCommand(f"forceload remove {from_} {to}")
        else:
            return CustomCommand(f"forceload remove {from_}")