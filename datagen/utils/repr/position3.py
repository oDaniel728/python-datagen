from typing import Self


class Position3[N: int | float]():
    def __init__(self, x: N, y: N, z: N):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        return f"{self.x} {self.y} {self.z}"
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def to_list(self) -> list[N]:
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> tuple[N, N, N]:
        return (self.x, self.y, self.z)
        

    def get_x(self) -> N: return self.x
    def get_y(self) -> N: return self.y
    def get_z(self) -> N: return self.z
    def set_x(self, x: N) -> None: self.x = x
    def set_y(self, y: N) -> None: self.y = y
    def set_z(self, z: N) -> None: self.z = z