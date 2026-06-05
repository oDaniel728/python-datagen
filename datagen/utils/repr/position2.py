from datagen.utils.repr.position3 import Position3


class Position2[N: int | float](Position3[N]):
    def __init__(self, x: N, z: N):
        super().__init__(x, 0, z) # type: ignore