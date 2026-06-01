from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datagen.utils.minecraft.BlockPosition import BlockPosition

class PlayerPosition():
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def relative_to(other: "PlayerPosition", x: float, y: float, z: float):
        return PlayerPosition(other.x + x, other.y + y, other.z + z)
    
    def to_string(self) -> str:
        return f"{self.x} {self.y} {self.z}"
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    def to_block_position(self) -> "BlockPosition":
        from datagen.utils.minecraft.BlockPosition import BlockPosition
        return BlockPosition(int(self.x), int(self.y), int(self.z))