from datagen.utils.minecraft.identifier import Identifier


class Enchantment():
    def __init__(self, id: Identifier, max_level: int = -1):
        self.id = id
        self.max_level = max_level

    def __str__(self) -> str:
        return str(self.id)

    def __invert__(self) -> str:
        return str(self.id)

    def to_dict(self) -> dict:
        return {"id": str(self.id), "max_level": self.max_level}