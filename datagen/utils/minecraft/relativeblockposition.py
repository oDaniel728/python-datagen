from datagen.utils.minecraft.blockposition import BlockPosition


class RelativeBlockPosition(BlockPosition):
    def __init__(self, x: int, y: int, z: int) -> None:
        super().__init__(x, y, z)

    def to_string(self) -> str:
        return f"~{self.x if self.x != 0 else ''}\
                 ~{self.y if self.y != 0 else ''}\
                 ~{self.z if self.z != 0 else ''}"