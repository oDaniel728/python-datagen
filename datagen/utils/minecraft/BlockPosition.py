from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datagen.utils.minecraft.PlayerPosition import PlayerPosition

class BlockPosition():
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def relative_to(other: "BlockPosition", x: int, y: int, z: int):
        return BlockPosition(other.x + x, other.y + y, other.z + z)
    
    def to_string(self) -> str:
        return f"{self.x} {self.y} {self.z}"
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def to_list(self) -> list[int]:
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)
    
    def to_player_position(self) -> "PlayerPosition":
        from datagen.utils.minecraft.PlayerPosition import PlayerPosition
        return PlayerPosition(float(self.x), float(self.y), float(self.z))