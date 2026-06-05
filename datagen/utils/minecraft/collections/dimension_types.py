from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.dimension_type import DimensionType

class DimensionTypes():
    OVERWORLD_CAVES = DimensionType(Identifier.of('minecraft:overworld_caves'))
    OVERWORLD = DimensionType(Identifier.of('minecraft:overworld'))
    THE_END = DimensionType(Identifier.of('minecraft:the_end'))
    THE_NETHER = DimensionType(Identifier.of('minecraft:the_nether'))
