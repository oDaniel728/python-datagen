from uuid import UUID

from datagen.extras.entities._util.hasproperties import HasProperties
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.repr.entitytype import EntityType


class BreedableEntities[T: HasProperties]:
    def with_age(self: T, age: int) -> T:
        self.properties['Age'] = age
        return self
    
    def with_forced_age(self: T, age: int) -> T:
        self.properties['ForcedAge'] = age
        return self
    
    def with_inlove(self: T, inlove: int) -> T:
        self.properties['InLove'] = inlove
        return self
    
    def with_love_cause(self: T, love_cause: UUID) -> T:
        self.properties['LoveCause'] = str(love_cause)
        return self