from datagen.types.util.holder import Holder
from datagen.utils.minecraft.identifier import Identifier


class ParticleType(Holder[Identifier]):
    def __init__(self, id: Identifier) -> None:
        super().__init__(id)

    def __str__(self) -> str:
        return str(self.get())