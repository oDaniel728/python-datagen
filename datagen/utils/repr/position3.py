from typing import Any, Type

from datagen.function.functionmacroargument import FunctionMacroArgument

class Position3[N: int | float | str | FunctionMacroArgument]():
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
    def get_x_as[T](self, t: Type[T]) -> T: return self.x # type: ignore
    def get_y_as[T](self, t: Type[T]) -> T: return self.y # type: ignore
    def get_z_as[T](self, t: Type[T]) -> T: return self.z # type: ignore
    def set_x(self, x: N) -> None: self.x = x
    def set_y(self, y: N) -> None: self.y = y
    def set_z(self, z: N) -> None: self.z = z

    @staticmethod
    def auto(v: Any) -> "Position3":
        if isinstance(v, Position3):
            return v
        elif isinstance(v, (list, tuple)) and len(v) == 3:
            return Position3(v[0], v[1], v[2])
        elif isinstance(v, dict) and all(k in v for k in ("x", "y", "z")):
            return Position3(v["x"], v["y"], v["z"])
        elif isinstance(v, str) and (s := v.split(" ")) and len(s) == 3:
            if ('$' in v) or ('~' in v):
                return Position3(s[0], s[1], s[2])
            elif '.' in v:
                return Position3(float(s[0]), float(s[1]), float(s[2]))
            else:
                return Position3(int(s[0]), int(s[1]), int(s[2]))
        else:
            raise ValueError(f"Cannot convert {v} to Position3")