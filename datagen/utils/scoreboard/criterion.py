from typing import Literal

from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item


class ObjectiveCriterion():
    TCriterion = Literal[
        "dummy",
        "trigger",
        "deathCount",
        "playerKillCount",
        "totalKillCount",
        "health",
        "food",
        "air",
        "armor",
        "xp",
        "level",
    ] | str
    DUMMY: "ObjectiveCriterion"
    TRIGGER: "ObjectiveCriterion"
    DEATH_COUNT: "ObjectiveCriterion"
    PLAYER_KILL_COUNT: "ObjectiveCriterion"
    TOTAL_KILL_COUNT: "ObjectiveCriterion"
    HEALTH: "ObjectiveCriterion"
    FOOD: "ObjectiveCriterion"
    AIR: "ObjectiveCriterion"
    ARMOR: "ObjectiveCriterion"
    XP: "ObjectiveCriterion"
    LEVEL: "ObjectiveCriterion"
    def __init__(self, value: TCriterion) -> None:
        self.value = value

    def to_string(self) -> str:
        return self.value

    @staticmethod
    def mined(block: Block) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.mined:{block.id.get_namespace()}.{block.id.get_path()}")
    
    @staticmethod
    def used(item: Item) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.used:{item.id.get_namespace()}.{item.id.get_path()}")

    @staticmethod
    def crafted(item: Item) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.crafted:{item.id.get_namespace()}.{item.id.get_path()}")
    
    @staticmethod
    def broken(item: Item) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.broken:{item.id.get_namespace()}.{item.id.get_path()}")
    
    @staticmethod
    def picked_up(item: Item) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.picked_up:{item.id.get_namespace()}.{item.id.get_path()}")
    
    @staticmethod
    def dropped(item: Item) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.dropped:{item.id.get_namespace()}.{item.id.get_path()}")
    
    @staticmethod
    def killed(entity: EntityType) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.killed:{entity.id.get_namespace()}.{entity.id.get_path()}")

    @staticmethod
    def killed_by(entity: EntityType) -> "ObjectiveCriterion":
        return ObjectiveCriterion(f"minecraft.killed_by:{entity.id.get_namespace()}.{entity.id.get_path()}")

    TCustomCriterion = Literal[
        "minecraft.jump",
        "minecraft.walk_one_cm",
        "minecraft.sprint_one_cm",
        "minecraft.crouch_one_cm",
        "minecraft.play_time",
        "minecraft.time_since_death",
        "minecraft.damage_dealt",
        "minecraft.damage_taken",
        "minecraft.talked_to_villager",
        "minecraft.traded_with_villager",
        "minecraft.leave_game",
        "minecraft.mob_kills",
        "minecraft.animals_bred",
    ]
    @staticmethod
    def custom(value: TCustomCriterion | str) -> "ObjectiveCriterion":
        return ObjectiveCriterion("minecraft.custom:" + value)

ObjectiveCriterion.DUMMY = ObjectiveCriterion("dummy")
ObjectiveCriterion.TRIGGER = ObjectiveCriterion("trigger")
ObjectiveCriterion.DEATH_COUNT = ObjectiveCriterion("deathCount")
ObjectiveCriterion.PLAYER_KILL_COUNT = ObjectiveCriterion("playerKillCount")
ObjectiveCriterion.TOTAL_KILL_COUNT = ObjectiveCriterion("totalKillCount")
ObjectiveCriterion.HEALTH = ObjectiveCriterion("health")
ObjectiveCriterion.FOOD = ObjectiveCriterion("food")
ObjectiveCriterion.AIR = ObjectiveCriterion("air")
ObjectiveCriterion.ARMOR = ObjectiveCriterion("armor")
ObjectiveCriterion.XP = ObjectiveCriterion("xp")
ObjectiveCriterion.LEVEL = ObjectiveCriterion("level")