from uuid import UUID

from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.repr.entitytype import EntityType


class AngerEntities(MobEntity):
    def __init__(self, type: EntityType):
        super().__init__(type)

    def with_anger_time(self, anger_time: int):
        self.properties["AngerTime"] = anger_time
        return self
    
    def with_angry_at(self, angry_at: UUID):
        self.properties["AngryAt"] = angry_at
        return self