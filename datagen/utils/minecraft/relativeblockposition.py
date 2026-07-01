from typing import override

from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.blockposition import BlockPosition


class RelativeBlockPosition(BlockPosition):
    def __init__(self, x: int | FunctionMacroArgument, y: int | FunctionMacroArgument, z: int | FunctionMacroArgument) -> None:
        super().__init__(x, y, z)

    @override
    def to_string(self) -> str:
        return f"~{self.x if self.x != 0 else ''} ~{self.y if self.y != 0 else ''} ~{self.z if self.z != 0 else ''}"
    
    def __str__(self) -> str:
        return self.to_string()