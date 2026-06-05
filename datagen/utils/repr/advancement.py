from datagen.types.util.holder import Holder
from datagen.utils.minecraft.identifier import Identifier


class Advancement(Holder[Identifier]):
    def __init__(self, id: Identifier):
        super().__init__(id)