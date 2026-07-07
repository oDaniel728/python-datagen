from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class GoatEntity(BaseEntity, MobEntity, BreedableEntities):
    def __init__(self):
        super().__init__(EntityTypes.GOAT)

    def with_has_left_horn(self, has_left_horn: bool) -> "GoatEntity":
        """
        If true, indicates this goat has the left horn.
        """
        self.properties["HasLeftHorn"] = has_left_horn
        return self

    def with_has_right_horn(self, has_right_horn: bool) -> "GoatEntity":
        """
        If true, indicates this goat has the right horn.
        """
        self.properties["HasRightHorn"] = has_right_horn
        return self

    def with_is_screaming_goat(self, is_screaming_goat: bool) -> "GoatEntity":
        """
        If true, indicates this is a screaming goat.
        """
        self.properties["IsScreamingGoat"] = is_screaming_goat
        return self
