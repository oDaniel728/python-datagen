class Position3[N: int | float]():
    def __init__(self, x: N, y: N, z: N):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.z}"
        