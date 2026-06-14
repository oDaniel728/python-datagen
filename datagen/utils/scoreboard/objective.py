from typing import TYPE_CHECKING, Literal, Self

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
if TYPE_CHECKING:
    from datagen.utils.scoreboard.player import ScoreboardPlayer

class ScoreboardObjective():
    TEMP: "ScoreboardObjective"
    #region types
    TDisplaySlot = Literal[
        "sidebar",
        "below_name",
        "list",
        "sidebar.team.black",
        "sidebar.team.dark_blue",
        "sidebar.team.dark_green",
        "sidebar.team.dark_aqua",
        "sidebar.team.dark_red",
        "sidebar.team.dark_purple",
        "sidebar.team.gold",
        "sidebar.team.gray",
        "sidebar.team.dark_gray",
        "sidebar.team.blue",
        "sidebar.team.green",
        "sidebar.team.aqua",
        "sidebar.team.red",
        "sidebar.team.light_purple",
        "sidebar.team.yellow",
        "sidebar.team.white",
    ] | str
    #endregion
    
    def __init__(
        self, 
        name: str,
        display_name: Text.BaseText, 
        criterion: ObjectiveCriterion = ObjectiveCriterion.DUMMY
    ) -> None:
        self.name = name
        self.display_name = display_name
        self.criterion = criterion

    def __str__(self) -> str: return self.name
    def to_string(self) -> str: return str(self)

    # Command Generators

    def add(self):
        return CustomCommand(
            "scoreboard objectives add", 
            self.name, 
            self.criterion.to_string(),
            self.display_name.to_string()
        )
    
    def remove(self):
        return CustomCommand(
            "scoreboard objectives remove", 
            self.name
        )
    
    def set_display(self, slot: TDisplaySlot):
        return CustomCommand(
            "scoreboard objectives setdisplay", 
            slot, 
            self.name
        )
    
    @staticmethod
    def clear_display(slot: TDisplaySlot):
        return CustomCommand(
            "scoreboard objectives setdisplay", 
            slot
        )
    
    @staticmethod
    def list_objectives():
        return CustomCommand("scoreboard objectives list")
    
    def modify_display_name(self, display_name: Text.BaseText):
        return CustomCommand(
            "scoreboard objectives modify", 
            self.name, 
            "displayname", 
            display_name.to_string()
        )
    
    def modify_display_auto_update(self, value: bool):
        return CustomCommand(
            "scoreboard objectives modify", 
            self.name, 
            "displayauto", 
            "true" if value else "false"
        )
    
    def modify_render_type(self, render_type: Literal["integer", "hearts"]):
        return CustomCommand(
            "scoreboard objectives modify", 
            self.name, 
            "rendertype", 
            render_type
        )
    
    def player(self, name: str | TargetSelector = "value") -> "ScoreboardPlayer":
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        return ScoreboardPlayer(self, name)
    
    def __invert__(self) -> "Self":
        ~ self.add()
        return self
    
ScoreboardObjective.TEMP = ScoreboardObjective("temp", Text.literal("Temporary Objective"), ObjectiveCriterion.DUMMY)