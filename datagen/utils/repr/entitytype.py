from datagen.utils.minecraft.identifier import Identifier


class EntityType():
    def __init__(self, id: Identifier):
        self.id = id

    def __str__(self) -> str:
        return str(self.id)