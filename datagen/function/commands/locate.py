from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.biome import Biome


class Locate():
    @staticmethod
    def biome(biome: Biome):
        return CustomCommand(f"locate biome {biome}")
    
    @staticmethod
    def poi(poi: Identifier):
        return CustomCommand(f"locate poi {poi}")

    @staticmethod
    def structure(structure: Identifier):
        return CustomCommand(f"locate structure {structure}")