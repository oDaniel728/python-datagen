from typing import Literal

from datagen.function.commands.customcommand import CustomCommand
from datagen.function.function import Function
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.scoreboard.objective import ScoreboardObjective


class ScoreboardPlayer():
    def __init__(self, objective: ScoreboardObjective, name: str | TargetSelector) -> None:
        self.objective = objective
        self.name = name

    def __str__(self) -> str: return str(self.name)
    def to_string(self) -> str: return str(self)

    def add(self, score: "int | ScoreboardPlayer"):
        if isinstance(score, int):
            return CustomCommand(
                "scoreboard players add", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        else:
            return self.operation(score, "+=")
    
    def remove(self, score: "int | ScoreboardPlayer"):
        if isinstance(score, int):
            return CustomCommand(
                "scoreboard players remove", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        else:
            return self.operation(score, "-=")

    def set(self, score: "int | ScoreboardPlayer"):
        if isinstance(score, int):
            return CustomCommand(
                "scoreboard players set", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        else:
            return self.operation(score, "=")
        
    def multiply(self, score: "int | ScoreboardPlayer") -> "CustomCommand":
        from datagen.utils.minecraft.text import Text
        out = CustomCommand()
        # 1. score add temp
        # 2. score player temp = 0
        # 3. score player temp += score
        # 4. score player self *= temp
        # 6. score remove temp
        tmpscore = ScoreboardObjective("temp_multiply", Text.literal(""), self.objective.criterion)
        from datagen.function.function import Function
        current_function = getattr(Function, "_Function__current_function", None)
        try:
            Function._Function__current_function = None # type: ignore
            out += tmpscore.add()
            tmp = tmpscore.player()
            out += tmp.set(0)
            out += tmp.add(score)
            out += self.operation(tmp, "*=")
            out += tmpscore.remove()
        finally:
            Function._Function__current_function = current_function # type: ignore
        return out
    
    def divide(self, score: "int | ScoreboardPlayer"):
        from datagen.utils.minecraft.text import Text
        out = CustomCommand()
        # 1. score add temp
        # 2. score player temp = 0
        # 3. score player temp += score
        # 4. score player self /= temp
        # 6. score remove temp
        tmpscore = ScoreboardObjective("temp_divide", Text.literal(""), self.objective.criterion)
        from datagen.function.function import Function
        current_function = getattr(Function, "_Function__current_function", None)
        try:
            Function._Function__current_function = None # type: ignore
            out += tmpscore.add()
            tmp = tmpscore.player()
            out += tmp.set(0)
            out += tmp.add(score)
            out += self.operation(tmp, "/=")
            out += tmpscore.remove()
        finally:
            Function._Function__current_function = current_function # type: ignore
        return out
    
    def modulus(self, score: "int | ScoreboardPlayer"):
        from datagen.utils.minecraft.text import Text
        out = CustomCommand()
        # 1. score add temp
        # 2. score player temp = 0
        # 3. score player temp += score
        # 4. score player self %= temp
        # 6. score remove temp
        tmpscore = ScoreboardObjective("temp_mod", Text.literal(""), self.objective.criterion)
        from datagen.function.function import Function
        current_function = getattr(Function, "_Function__current_function", None)
        try:
            Function._Function__current_function = None # type: ignore
            out += tmpscore.add()
            tmp = tmpscore.player()
            out += tmp.set(0)
            out += tmp.add(score)
            out += self.operation(tmp, "%=")
            out += tmpscore.remove()
        finally:
            Function._Function__current_function = current_function # type: ignore
        return out

    def swap(self, score: "ScoreboardPlayer"):
        out = CustomCommand()
        out += self.operation(score, "><")
        return out
    
    def min(self, score: "ScoreboardPlayer"):
        out = CustomCommand()
        out += self.operation(score, "<")
        return out
    
    def max(self, score: "ScoreboardPlayer"):
        out = CustomCommand()
        out += self.operation(score, ">")
        return out

    def reset(self):
        return CustomCommand(
            "scoreboard players reset", 
            str(self), 
            str(self.objective)
        )
    
    def enable(self):
        return CustomCommand(
            "scoreboard players enable", 
            str(self), 
            str(self.objective)
        )
    
    def display_name(self, name: str):
        return CustomCommand(
            "scoreboard players display name", 
            str(self), 
            str(name)
        )

    TOperation = Literal["+=", "-=", "*=", "/=", "%=", "><", "=", "<", ">", "!="]
    def operation(self, target: "ScoreboardPlayer", operation: TOperation):
        return CustomCommand(
            "scoreboard players operation", 
            str(self), 
            str(self.objective), 
            operation, 
            str(target), 
            str(target.objective)
        )

    @staticmethod
    def all_from(objective: ScoreboardObjective):
        return ScoreboardPlayer(objective, '*')