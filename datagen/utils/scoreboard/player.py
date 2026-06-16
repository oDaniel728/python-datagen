from typing import TYPE_CHECKING, Any, Literal, Self

from datagen.function.commands.customcommand import CustomCommand
if TYPE_CHECKING:
    from datagen.function.function import Function
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.scoreboard.objective import ScoreboardObjective


class ScoreboardPlayer():
    def __init__(self, objective: ScoreboardObjective, name: str | TargetSelector) -> None:
        self.objective = objective
        self.name = name

    def to_identiifer(self) -> Identifier:
        return Identifier.of(self.objective.name, str(self.name).replace("@", "at_").replace("\n#", "hs_"))

    def __str__(self) -> str: return str(self.name)
    def to_string(self) -> str: return str(self)

    def add(self, score: "int | ScoreboardPlayer | FunctionMacroArgument"):
        if isinstance(score, (int, FunctionMacroArgument)):
            return CustomCommand(
                f"\n# add {~self.to_identiifer()} {score}\n",
                "\tscoreboard players add", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        else:
            return self.operation(score, "+=")
    
    def remove(self, score: "int | ScoreboardPlayer | FunctionMacroArgument"):
        if isinstance(score, (int, FunctionMacroArgument)):
            return CustomCommand(
                f"\n# remove {~self.to_identiifer()} {score}\n",
                "\tscoreboard players remove", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        else:
            return self.operation(score, "-=")

    def set(self, score: "int | ScoreboardPlayer | FunctionMacroArgument | Function"):
        from datagen.function.function import Function
        if isinstance(score, (int, FunctionMacroArgument)):
            return CustomCommand(
                f"\n# set {~self.to_identiifer()} {score}\n",
                "\tscoreboard players set", 
                str(self), 
                str(self.objective), 
                str(score)
            )
        elif isinstance(score, Function):
            return CustomCommand(
                f"\n# set {~self.to_identiifer()} {score}\n",
                "execute store result score", 
                str(self), 
                str(self.objective), 
                "int 1 run function", 
                str(score)
            )
        else:
            return self.operation(score, "=")
        
    def multiply(self, score: "int | ScoreboardPlayer | FunctionMacroArgument") -> "CustomCommand":
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
            out += f"\n# multiply {self.name} {str(score)}"
            Function._Function__current_function = None # type: ignore
            out += tmpscore.add()
            tmp = tmpscore.player()
            out += tmp.set(score)
            out += self.operation(tmp, "*=")
            out += tmpscore.remove()
        finally:
            Function._Function__current_function = current_function # type: ignore
        return out
    
    def divide(self, score: "int | ScoreboardPlayer | FunctionMacroArgument"):
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
            out += f"\n# divide {self.name} {str(score)}"
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
    
    def modulus(self, score: "int | ScoreboardPlayer | FunctionMacroArgument"):
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
            out += f"\n# modulus {self.name} {str(score)}"
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
        out += f"\n# swap {self.name} {score.name}\n"
        out += self.operation(score, "><")
        return out
    
    def min(self, score: "ScoreboardPlayer"):
        out = CustomCommand()
        out += f"\n# min {self.name} {score.name}\n"
        out += self.operation(score, "<")
        return out
    
    def max(self, score: "ScoreboardPlayer"):
        out = CustomCommand()
        out += f"\n# max {self.name} {score.name}\n"
        out += self.operation(score, ">")
        return out

    def reset(self):
        return CustomCommand(
            f"\n# reset {self.name}\n",
            "scoreboard players reset", 
            str(self), 
            str(self.objective)
        )
    
    def enable(self):
        return CustomCommand(
            f"\n# enable {self.name}\n",
            "scoreboard players enable", 
            str(self), 
            str(self.objective)
        )
    
    def display_name(self, name: str):
        return CustomCommand(
            f"\n# display name {self.name} {name}\n",
            "scoreboard players display name", 
            str(self), 
            str(name)
        )

    TOperation = Literal["+=", "-=", "*=", "/=", "%=", "><", "=", "<", ">", "!="]
    def operation(self, target: "ScoreboardPlayer", operation: TOperation):
        return CustomCommand(
            f"\n# {self.name} {operation} {target.name}\n",
            "scoreboard players operation", 
            str(self), 
            str(self.objective), 
            operation, 
            str(target), 
            str(target.objective)
        )

    def get(self):
        out = CustomCommand()
        out += f"# get {self.name}"
        out += f"scoreboard players get {self} {self.objective}"
        return out

    @staticmethod
    def all_from(objective: ScoreboardObjective):
        return ScoreboardPlayer(objective, '*')