from datagen.function.commands.scoreboard import Scoreboard
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective

COIN_HEALTHS: ScoreboardObjective = Scoreboard.objective("coin_healths", LiteralText.EMPTY, ObjectiveCriterion.DUMMY)