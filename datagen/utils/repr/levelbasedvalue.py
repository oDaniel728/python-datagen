from datagen.types.protocols.todict import ToDict

class LevelBasedValue(ToDict): ...

class _Linear(LevelBasedValue):
    def __init__(self, base: float, per_level_above_first: float):
        self.base = base
        self.per_level_above_first = per_level_above_first

    def to_dict(self) -> dict:
        return {
            "type": "minecraft:linear",
            "base": self.base,
            "per_level_above_first": self.per_level_above_first
        }

class _LevelsSquared(LevelBasedValue):
    def __init__(self, added: float = 0):
        self.added = added

    def to_dict(self) -> dict:
        return {
            "type": "minecraft:levels_squared",
            "added": self.added
        }

class _Clamped(LevelBasedValue):
    def __init__(self, value, min: float, max: float):
        self.value = LevelBasedValues._lift(value)
        self.min = min
        self.max = max

    def to_dict(self) -> dict:
        return {
            "type": "minecraft:clamped",
            "value": LevelBasedValues._dictify(self.value),
            "min": self.min,
            "max": self.max
        }

class _Fraction(LevelBasedValue):
    def __init__(self, numerator, denominator):
        self.numerator = LevelBasedValues._lift(numerator)
        self.denominator = LevelBasedValues._lift(denominator)

    def to_dict(self) -> dict:
        return {
            "type": "minecraft:fraction",
            "numerator": LevelBasedValues._dictify(self.numerator),
            "denominator": LevelBasedValues._dictify(self.denominator)
        }

class _Lookup(LevelBasedValue):
    def __init__(self, values: list[float], fallback: float | None = None):
        self.values = values
        self.fallback = fallback

    def to_dict(self) -> dict:
        d: dict = {
            "type": "minecraft:lookup",
            "values": self.values
        }
        if self.fallback is not None:
            d["fallback"] = self.fallback
        return d

class LevelBasedValues(ToDict):
    @staticmethod
    def constant(value: float) -> float:
        return value

    @staticmethod
    def linear(base: float, per_level_above_first: float) -> "LevelBasedValue":
        return _Linear(base, per_level_above_first)

    @staticmethod
    def levels_squared(added: float = 0) -> "LevelBasedValue":
        return _LevelsSquared(added)

    @staticmethod
    def clamped(value, min: float, max: float) -> "LevelBasedValue":
        return _Clamped(value, min, max)

    @staticmethod
    def fraction(numerator, denominator) -> "LevelBasedValue":
        return _Fraction(numerator, denominator)

    @staticmethod
    def lookup(values: list[float], fallback: float | None = None) -> "LevelBasedValue":
        return _Lookup(values, fallback)

    @staticmethod
    def _lift(value: float | ToDict) -> ToDict | float:
        if isinstance(value, (int, float)):
            return float(value)
        return value

    @staticmethod
    def _dictify(value) -> dict | float:
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value

def as_level(value: float | ToDict) -> dict | float:
    if isinstance(value, ToDict):
        return value.to_dict()
    return value
