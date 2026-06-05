from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.fluid import Fluid

class Fluids():
    LAVA = Fluid(Identifier.of('minecraft:lava'))
    EMPTY = Fluid(Identifier.of('minecraft:empty'))
    WATER = Fluid(Identifier.of('minecraft:water'))
    FLOWING_LAVA = Fluid(Identifier.of('minecraft:flowing_lava'))
    FLOWING_WATER = Fluid(Identifier.of('minecraft:flowing_water'))
