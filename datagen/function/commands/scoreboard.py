from datagen.function.commands.command import Command
class ScoreBoard():
    class Players():
        @staticmethod
        def operation(target_obj, target_player, source_obj, source_player, operation):
            return ScoreboardPlayerOperation(target_obj, target_player, source_obj, source_player, operation)
        
        @staticmethod
        def add(objective: str, player: str, value: int):
            return ScoreboardPlayerAdd(objective, player, value)
        
        @staticmethod
        def set(objective: str, player: str, value: int):
            return ScoreboardPlayerSet(objective, player, value)
    class Objectives():
        @staticmethod
        def add(objective: str, criterion: str = "dummy"):
            return ScoreboardObjectiveAdd(objective, criterion)

class ScoreboardPlayerOperation(Command):
    def __init__(self, target_obj, target_player, source_obj, source_player, operation):
        self.target_obj = target_obj
        self.target_player = target_player
        self.source_obj = source_obj
        self.source_player = source_player
        self.operation = operation

    def to_string(self) -> str:
        return f"scoreboard players operation {self.target_player} {self.target_obj} {self.operation} {self.source_player} {self.source_obj}"
class ScoreboardPlayerAdd(Command):
    def __init__(self, objective: str, player: str, value: int):
        self.objective = objective
        self.player = player
        self.value = value

    def to_string(self) -> str:
        return f"scoreboard players add {self.player} {self.objective} {self.value}"
class ScoreboardPlayerSet(Command):
    def __init__(self, objective: str, player: str, value: int):
        self.objective = objective
        self.player = player
        self.value = value

    def to_string(self) -> str:
        return f"scoreboard players set {self.player} {self.objective} {self.value}"
class ScoreboardObjectiveAdd(Command):
    def __init__(self, objective: str, criterion: str = "dummy"):
        self.objective = objective
        self.criterion = criterion

    def to_string(self) -> str:
        return f"scoreboard objectives add {self.objective} {self.criterion}"