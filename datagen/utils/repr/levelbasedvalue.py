from datagen.types.protocols.todict import ToDict


class LevelBasedValue(ToDict):
    @staticmethod
    def constant(value: float) -> float:
        return value

    @staticmethod
    def linear(base: float, per_level_above_first: float) -> "LevelBasedValue":
        return LevelBasedValue._Linear(base, per_level_above_first)

    @staticmethod
    def levels_squared(added: float = 0) -> "LevelBasedValue":
        return LevelBasedValue._LevelsSquared(added)

    @staticmethod
    def clamped(value, min: float, max: float):
        return LevelBasedValue._Clamped(value, min, max)

    @staticmethod
    def fraction(numerator, denominator):
        return LevelBasedValue._Fraction(numerator, denominator)

    @staticmethod
    def lookup(values: list[float], fallback: float | None = None):
        return LevelBasedValue._Lookup(values, fallback)

    class _Linear(ToDict):
        def __init__(self, base: float, per_level_above_first: float):
            self.base = base
            self.per_level_above_first = per_level_above_first

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:linear",
                "base": self.base,
                "per_level_above_first": self.per_level_above_first
            }

    class _LevelsSquared(ToDict):
        def __init__(self, added: float = 0):
            self.added = added

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:levels_squared",
                "added": self.added
            }

    class _Clamped(ToDict):
        def __init__(self, value, min: float, max: float):
            self.value = LevelBasedValue._lift(value)
            self.min = min
            self.max = max

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:clamped",
                "value": LevelBasedValue._dictify(self.value),
                "min": self.min,
                "max": self.max
            }

    class _Fraction(ToDict):
        def __init__(self, numerator, denominator):
            self.numerator = LevelBasedValue._lift(numerator)
            self.denominator = LevelBasedValue._lift(denominator)

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:fraction",
                "numerator": LevelBasedValue._dictify(self.numerator),
                "denominator": LevelBasedValue._dictify(self.denominator)
            }

    class _Lookup(ToDict):
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
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value
