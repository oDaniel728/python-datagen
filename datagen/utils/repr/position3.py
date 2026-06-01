class Position3[N: int | float]():
    def __init__(self, x: N, y: N, z: N):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z}"

    def to_string(self) -> str:
        return f"{self.x} {self.y} {self.z}"
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def to_list(self) -> list[N]:
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> tuple[N, N, N]:
        return (self.x, self.y, self.z)
        