class EnchantedChance():
    def __init__(self, data: float | dict):
        self._data = data

    @staticmethod
    def constant(chance: float) -> "EnchantedChance":
        return EnchantedChance(chance)

    @staticmethod
    def linear(base: float, per_level_above_first: float) -> "EnchantedChance":
        return EnchantedChance({
            "type": "minecraft:linear",
            "base": base,
            "per_level_above_first": per_level_above_first
        })

    def to_dict(self) -> float | dict:
        return self._data
