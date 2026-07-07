from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class BlazeEntity(MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.BLAZE)