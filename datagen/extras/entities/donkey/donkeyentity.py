from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.breedableentities import BreedableEntities
from datagen.extras.entities.mobentity import MobEntity
from datagen.extras.entities.ownableentities import OwnableEntities
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.itemstack import ItemStack


class DonkeyEntity(BaseEntity, MobEntity, BreedableEntities, OwnableEntities):
    def __init__(self):
        super().__init__(EntityTypes.DONKEY)

    def with_bred(self, bred: bool) -> "DonkeyEntity":
        """
        Whether or not the donkey has been bred.
        If true, the donkey will not breed again until it has grown up and the breeding cooldown has passed.
        """
        self.properties["Bred"] = bred
        return self
    
    def with_eating_haystack(self, eating_haystack: bool) -> "DonkeyEntity":
        """
        Whether or not the donkey is currently eating a haystack.
        If true, the donkey will be in the eating animation and will not move.
        """
        self.properties["EatingHaystack"] = eating_haystack
        return self
    
    def with_tame(self, tame: bool) -> "DonkeyEntity":
        """
        Whether or not the donkey is tamed.
        If true, the donkey will not despawn and can be ridden by the player.
        """
        self.properties["Tame"] = tame
        return self
    
    def with_temper(self, temper: int) -> "DonkeyEntity":
        """
        The donkey's temper.
        If the donkey is not tamed, this value will increase when the player attempts to ride it.
        When it reaches 0, the donkey will become tamed and the player will be able to ride it.
        """
        self.properties["Temper"] = temper
        return self
    
    def with_chested_horse(self, chested_horse: bool) -> "DonkeyEntity":
        """
        Whether or not the donkey has a chest.
        If true, the donkey will have an inventory and can be used to carry items.
        """
        self.properties["ChestedHorse"] = chested_horse
        return self
    
    def with_items(self, items: list[ItemStack]) -> "DonkeyEntity":
        """
        The items in the donkey's inventory.
        If the donkey has a chest, this will be a list of items in the chest.
        If the donkey does not have a chest, this will be an empty list.
        """
        self.properties["Items"] = items
        return self
