from uuid import UUID

from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.repr.entitytype import EntityType


class BreedableEntities(MobEntity):
    def __init__(self, type: EntityType):
        super().__init__(type)

    def with_age(self, age: int):
        self.properties['Age'] = age
        return self
    
    def with_forced_age(self, age: int):
        self.properties['ForcedAge'] = age
        return self
    
    def with_inlove(self, inlove: int):
        self.properties['InLove'] = inlove
        return self
    
    def with_love_cause(self, love_cause: UUID):
        self.properties['LoveCause'] = str(love_cause)
        return self