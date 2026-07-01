from typing import TYPE_CHECKING

from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.repr.position3 import Position3


if TYPE_CHECKING:
    from datagen.utils.minecraft.playerposition import PlayerPosition

class BlockPosition(Position3[int | FunctionMacroArgument]):
    def __init__(self, x: int | FunctionMacroArgument, y: int | FunctionMacroArgument, z: int | FunctionMacroArgument):
        super().__init__(x, y, z)

    @staticmethod
    def pos2(x: int, z: int) -> 'BlockPosition':
        return BlockPosition(x, 0, z)