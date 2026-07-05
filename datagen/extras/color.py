class Color():
    def __init__(self, value: int):
        self._v = value

    def to_int(self) -> int:
        return self._v
    
    def to_decimal(self) -> float:
        return self._v / 255.0
    
    def __int__(self) -> int:
        return self.to_int()
    
    def __str__(self) -> str:
        return self.to_hex()
    
    def __repr__(self) -> str:
        return f'Color({self._v})'
    
    def __float__(self):
        return self.to_decimal()
    
    def __bool__(self):
        return self._v != 0
    
    def to_hex(self) -> str:
        return f'#{self._v:06x}'
    
    def to_rgb(self) -> tuple[int, int, int]:
        r = (self._v >> 16) & 0xFF
        g = (self._v >> 8) & 0xFF
        b = self._v & 0xFF
        return (r, g, b)
    
    @staticmethod
    def from_hex(hex_str: str) -> 'Color':
        if hex_str.startswith('#'):
            hex_str = hex_str[1:]
        value = int(hex_str, 16)
        return Color(value)
    
    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> 'Color':
        value = (r << 16) | (g << 8) | b
        return Color(value)
    
    @staticmethod
    def from_decimal(decimal: float) -> 'Color':
        value = int(decimal * 255)
        return Color(value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self._v == other._v
        return str(self) == str(other)
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash(self._v)