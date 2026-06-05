from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.villager_type import VillagerType

class VillagerTypes():
    SNOW = VillagerType(Identifier.of('minecraft:snow'))
    DESERT = VillagerType(Identifier.of('minecraft:desert'))
    PLAINS = VillagerType(Identifier.of('minecraft:plains'))
    JUNGLE = VillagerType(Identifier.of('minecraft:jungle'))
    TAIGA = VillagerType(Identifier.of('minecraft:taiga'))
    SAVANNA = VillagerType(Identifier.of('minecraft:savanna'))
    SWAMP = VillagerType(Identifier.of('minecraft:swamp'))
