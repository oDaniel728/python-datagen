from datagen.utils.minecraft.identifier import Identifier


class ParticleType():
    def __init__(self, id: Identifier) -> None:
        self.id = id

    def __str__(self) -> str:
        return str(self.id)