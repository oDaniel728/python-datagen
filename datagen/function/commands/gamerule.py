
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.repr.gamerule import MCGamerule


class Gamerule():
    @staticmethod
    def set(gamerule: MCGamerule, value: bool | int | str) -> CustomCommand:
        return CustomCommand(f"gamerule {gamerule} {value}")
    
    @staticmethod
    def get(gamerule: MCGamerule) -> CustomCommand:
        return CustomCommand(f"gamerule {gamerule}")