
from datagen.utils.minecraft.identifier import Identifier


class EntityType():
    def __init__(self, id: Identifier):
        self.id = id

    def __str__(self) -> str:
        return str(self.id)
    
    def __neg__(self) -> "EntityType":
        return EntityType(Identifier.of(f"!{self.id}"))
    
    def NOT(self):
        return -self