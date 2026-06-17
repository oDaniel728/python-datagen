from calendar import c
from dataclasses import dataclass
import re
from typing import Literal

from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagen.utils.scoreboard.player import ScoreboardPlayer

class Scoreboard():
    @staticmethod
    def objective(
        name: str, 
        display_name: Text.BaseText, 
        criterion: ObjectiveCriterion = ObjectiveCriterion.DUMMY
    ) -> ScoreboardObjective:
        return ScoreboardObjective(name, display_name, criterion)
    
    @staticmethod
    def player(objective: ScoreboardObjective, name: str | TargetSelector):
        return objective.player(name)
    
    @staticmethod
    def literal(value: int) -> "ScoreboardPlayer":
        p = (~ ScoreboardObjective.TEMP)[f"__literal_{value}"]
        ~ p.set(value)
        return p