from datagen.extras.entities.armorstand.armorstandpose import ArmorStandPose
from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entitytype import EntityType


class ArmorStandEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.ARMOR_STAND)
    
    def with_invisible(self, invisible: bool) -> "ArmorStandEntity":
        self.properties["Invisible"] = invisible
        return self
    
    def with_marker(self, marker: bool) -> "ArmorStandEntity":
        self.properties["Marker"] = marker
        return self
    
    def with_small(self, small: bool) -> "ArmorStandEntity":
        self.properties["Small"] = small
        return self
    
    def with_no_base_plate(self, no_base_plate: bool) -> "ArmorStandEntity":
        self.properties["NoBasePlate"] = no_base_plate
        return self

    def with_pose(self, pose: "ArmorStandPose") -> "ArmorStandEntity":
        self.properties["Pose"] = pose.to_dict()
        return self
    
    CHANGING_MAINHAND = 2**0
    CHANGING_BOOTS = 2**1
    CHANGING_LEGGINGS = 2**2
    CHANGING_CHESTPLATE = 2**3
    CHANGING_HELMET = 2**4
    CHANGING_OFFHAND = 2**5

    REMOVING_MAINHAND = 2**8
    REMOVING_BOOTS = 2**9
    REMOVING_LEGGINGS = 2**10
    REMOVING_CHESTPLATE = 2**11
    REMOVING_HELMET = 2**12
    REMOVING_OFFHAND = 2**13

    ADDING_MAINHAND = 2**16
    ADDING_BOOTS = 2**17
    ADDING_LEGGINGS = 2**18
    ADDING_CHESTPLATE = 2**19
    ADDING_HELMET = 2**20
    ADDING_OFFHAND = 2**21

    def with_disabled_slots(self, disabled_slots: int) -> "ArmorStandEntity":
        self.properties["DisabledSlots"] = disabled_slots
        return self