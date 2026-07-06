from typing import Literal, Self
from uuid import UUID

from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.villager.tradeoffer import VillagerTradeOffer
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.repr.entityuuid import EntityUUID
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.villager_profession import VillagerProfession
from datagen.utils.repr.villager_type import VillagerType
from datagen.types.util.reprs import *


class VillagerEntity(BaseEntity):
    def __init__(self):
        super().__init__(EntityTypes.VILLAGER)

    def with_villager_type(self, type: VillagerType) -> Self:
        self.properties.setdefault("VillagerData", {})["type"] = type.id.to_string()
        return self

    def with_villager_profession(self, profession: VillagerProfession) -> Self:
        self.properties.setdefault("VillagerData", {})["profession"] = profession.id.to_string()
        return self

    def with_villager_level(self, level: int) -> Self:
        self.properties.setdefault("VillagerData", {})["level"] = level
        return self

    def with_villager_data(self, type: VillagerType, profession: VillagerProfession, level: int) -> Self:
        self.properties["VillagerData"] = {
            "type": type.id.to_string(),
            "profession": profession.id.to_string(),
            "level": level,
        }
        return self

    def get_villager_type(self) -> str | None:
        data = self.properties.get("VillagerData")
        if data is None:
            return None
        return data.get("type")

    def get_villager_profession(self) -> str | None:
        data = self.properties.get("VillagerData")
        if data is None:
            return None
        return data.get("profession")

    def get_villager_level(self) -> int | None:
        data = self.properties.get("VillagerData")
        if data is None:
            return None
        return data.get("level")

    def with_xp(self, value: int) -> Self:
        self.properties["Xp"] = value
        return self

    def get_xp(self) -> int | None:
        return self.properties.get("Xp")

    _TGossipType = Literal["major_negative", "minor_negative", "major_positive", "minor_positive", "trading"]

    def add_gossip(self, type: _TGossipType, value: int, target: tuple4[int] | EntityUUID | UUID) -> Self:
        if isinstance(target, UUID):
            target = EntityUUID.from_uuid(target)
        if isinstance(target, EntityUUID):
            target = [target._1, target._2, target._3, target._4]
        else:
            target = list[int](target)
        gossips = self.properties.setdefault("Gossips", [])
        gossips.append({"Type": type, "Value": value, "Target": target})
        return self

    def get_gossips(self) -> list[dict] | None:
        return self.properties.get("Gossips")

    def add_offer(self, offer: VillagerTradeOffer) -> Self:
        offers = self.properties.setdefault("Offers", {})
        recipes = offers.setdefault("Recipes", [])
        recipes.append(offer.to_dict())
        return self

    def get_offers(self) -> list[dict] | None:
        offers = self.properties.get("Offers")
        if offers is None:
            return None
        return offers.get("Recipes")

    def add_inventory_item(self, item: ItemStack) -> Self:
        inventory = self.properties.setdefault("Inventory", [])
        inventory.append(item.to_dict())
        return self

    def get_inventory(self) -> list[dict] | None:
        return self.properties.get("Inventory")

    def with_last_restock(self, value: int) -> Self:
        self.properties["LastRestock"] = value
        return self

    def get_last_restock(self) -> int | None:
        return self.properties.get("LastRestock")

    def with_last_gossip_decay(self, value: int) -> Self:
        self.properties["LastGossipDecay"] = value
        return self

    def get_last_gossip_decay(self) -> int | None:
        return self.properties.get("LastGossipDecay")

    def with_restocks_today(self, value: int) -> Self:
        self.properties["RestocksToday"] = value
        return self

    def get_restocks_today(self) -> int | None:
        return self.properties.get("RestocksToday")

    def with_willing(self, value: boolean) -> Self:
        self.properties["Willing"] = int(value)
        return self

    def get_willing(self) -> bool | None:
        value = self.properties.get("Willing")
        if value is None:
            return None
        return bool(value)

    def with_age(self, value: int) -> Self:
        self.properties["Age"] = value
        return self

    def get_age(self) -> int | None:
        return self.properties.get("Age")

    def with_forced_age(self, value: int) -> Self:
        self.properties["ForcedAge"] = value
        return self

    def get_forced_age(self) -> int | None:
        return self.properties.get("ForcedAge")

    def with_in_love(self, value: int) -> Self:
        self.properties["InLove"] = value
        return self

    def get_in_love(self) -> int | None:
        return self.properties.get("InLove")

    def with_love_cause(self, uuid: tuple4[int] | EntityUUID | UUID) -> Self:
        if isinstance(uuid, UUID):
            uuid = EntityUUID.from_uuid(uuid)
        if isinstance(uuid, EntityUUID):
            self.properties["LoveCauseLeast"] = uuid._1
            self.properties["LoveCauseMost"] = uuid._3
        else:
            values = list[int](uuid)
            self.properties["LoveCauseLeast"] = values[0]
            self.properties["LoveCauseMost"] = values[2]
        return self

    def get_love_cause(self) -> dict | None:
        least = self.properties.get("LoveCauseLeast")
        most = self.properties.get("LoveCauseMost")
        if least is None or most is None:
            return None
        return {"LoveCauseLeast": least, "LoveCauseMost": most}
