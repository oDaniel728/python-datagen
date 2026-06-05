from typing import Literal

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector


class Excerience():
    _TUnit = Literal["points", "levels"]

    @staticmethod
    def add(target: TargetSelector, amount: int, unit: _TUnit, /) -> CustomCommand:
        return CustomCommand(f"experience add {target} {amount} {unit}")
    
    @staticmethod
    def set(target: TargetSelector, amount: int, unit: _TUnit, /) -> CustomCommand:
        return CustomCommand(f"experience set {target} {amount} {unit}")
    
    @staticmethod
    def query(target: TargetSelector, type: Literal["points", "levels"], /) -> CustomCommand:
        return CustomCommand(f"experience query {target} {type}")