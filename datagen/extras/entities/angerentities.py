from uuid import UUID

from datagen.extras.entities._util.hasproperties import HasProperties
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.repr.entitytype import EntityType


class AngerEntities[T: HasProperties]:
    def with_anger_time(self: T, anger_time: int) -> T:
        self.properties["AngerTime"] = anger_time
        return self
    
    def with_angry_at(self: T, angry_at: UUID) -> T:
        self.properties["AngryAt"] = angry_at
        return self