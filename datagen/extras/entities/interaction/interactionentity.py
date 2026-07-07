from datagen.extras.entities.baseentity import BaseEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class InteractionEntity(BaseEntity):
    def __init__(self):
        super().__init__(EntityTypes.INTERACTION)

    def with_width(self, value: float) -> "InteractionEntity":
        self.properties["width"] = value
        return self

    def with_height(self, value: float) -> "InteractionEntity":
        self.properties["height"] = value
        return self

    def with_response(self, value: bool) -> "InteractionEntity":
        self.properties["response"] = value
        return self

    def with_attack(self, player_uuid: list[int], timestamp: int) -> "InteractionEntity":
        self.properties["attack"] = {"player": player_uuid, "timestamp": timestamp}
        return self

    def with_interaction(self, player_uuid: list[int], timestamp: int) -> "InteractionEntity":
        self.properties["interaction"] = {"player": player_uuid, "timestamp": timestamp}
        return self