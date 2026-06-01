from typing import TYPE_CHECKING

from datagen.utils.repr.position3 import Position3


if TYPE_CHECKING:
    from datagen.utils.minecraft.blockposition import BlockPosition

class RelativePlayerPosition(Position3[float]):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)

    def to_string(self) -> str:
        return f"~{self.x if self.x != 0 else ''} ~{self.y if self.y != 0 else ''} ~{self.z if self.z != 0 else ''}"

    def to_block_position(self) -> "BlockPosition":
        from datagen.utils.minecraft.blockposition import BlockPosition
        return BlockPosition(int(self.x), int(self.y), int(self.z))