from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.dimension import Dimension

class Dimensions():
    OVERWORLD_CAVES = Dimension(Identifier.of('minecraft:overworld_caves'))
    OVERWORLD = Dimension(Identifier.of('minecraft:overworld'))
    THE_END = Dimension(Identifier.of('minecraft:the_end'))
    THE_NETHER = Dimension(Identifier.of('minecraft:the_nether'))
