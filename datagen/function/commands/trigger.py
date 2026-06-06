from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.scoreboard.objective import ScoreboardObjective

class Trigger():
    @staticmethod
    def add(objective: ScoreboardObjective, amount: int = 1):
        return CustomCommand(f"trigger {objective} add {amount}")
    
    @staticmethod
    def set(objective: ScoreboardObjective, amount: int = 1):
        return CustomCommand(f"trigger {objective} set {amount}")