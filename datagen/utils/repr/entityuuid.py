from uuid import UUID
from datagen.types.protocols.tostring import ToString
from datagen.types.util.reprs import *

class EntityUUID(ToString):
    def __init__(self, _1: int, _2: int, _3: int, _4: int) -> None:
        self._1 = _1
        self._2 = _2
        self._3 = _3
        self._4 = _4

    @staticmethod
    def from_uuid(uuid: UUID) -> "EntityUUID":
        return EntityUUID(
            uuid.int >> 96 & 0xFFFFFFFF, 
            uuid.int >> 64 & 0xFFFFFFFF, 
            uuid.int >> 32 & 0xFFFFFFFF, 
            uuid.int & 0xFFFFFFFF
        )
    
    @staticmethod
    def from_tuple4(values: tuple4[int]) -> "EntityUUID":
        values = list[int](values)
        if len(values) != 4:
            raise ValueError(f"Expected a tuple of length 4, got {len(values)}")
        return EntityUUID(values[0], values[1], values[2], values[3])
    
    def to_uuid(self) -> UUID:
        return UUID(int=(self._1 << 96) | (self._2 << 64) | (self._3 << 32) | self._4)
    
    def to_string(self) -> str:
        return f"[I; {self._1}, {self._2}, {self._3}, {self._4}]"
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __setitem__(self, key: int, value: int):
        if not 0 <= key < 4:
            raise IndexError("Index out of range")
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        setattr(self, f"_{key + 1}", value)