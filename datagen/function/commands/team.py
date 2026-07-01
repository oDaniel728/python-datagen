from typing import Literal

from datagen.function.commands.customcommand import CustomCommand
from datagen.types.util.partialstring import PartialString
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text

class Team():
    @staticmethod
    def add(name: PartialString, displayName: Text.BaseText):
        return CustomCommand(f"team add {name} {displayName}")
    
    @staticmethod
    def empty(name: PartialString):
        return CustomCommand(f"team empty {name}")
    
    @staticmethod
    def join(name: PartialString, target: TargetSelector):
        return CustomCommand(f"team join {name} {target}")

    @staticmethod
    def leave(target: TargetSelector):
        return CustomCommand(f"team leave {target}")
    
    @staticmethod
    def list(name: PartialString | None = None):
        if name:
            return CustomCommand(f"team list {name}")
        return CustomCommand("team list")
    
    @staticmethod
    def remove(name: PartialString):
        return CustomCommand(f"team remove {name}")

    class _UTeamModifier():
        def __init__(self, name: PartialString) -> None:
            self.name = name

        def displayName(self, displayName: Text.BaseText):
            return CustomCommand(f"team modify {self.name} displayName {displayName}")
        
        def color(self, color: Text.BaseTextSettings.TextColor):
            return CustomCommand(f"team modify {self.name} color {color}")
        
        _TTeamCollisionRule = Literal["always", "never", "pushOtherTeams", "pushOwnTeam"]
        def collisionRule(self, rule: _TTeamCollisionRule):
            return CustomCommand(f"team modify {self.name} collisionRule {rule}")
        
        def friendlyFire(self, friendlyFire: bool):
            return CustomCommand(f"team modify {self.name} friendlyFire {str(friendlyFire).lower()}")
        
        _TVisibility = Literal["always", "never", "hideForOtherTeams", "hideForOwnTeam"]
        def deathMessageVisibility(self, visibility: _TVisibility):
            return CustomCommand(f"team modify {self.name} deathMessageVisibility {visibility}")
        
        def nametagVisibility(self, visibility: _TVisibility):
            return CustomCommand(f"team modify {self.name} nametagVisibility {visibility}")
        
        def prefix(self, prefix: Text.BaseText):
            return CustomCommand(f"team modify {self.name} prefix {prefix}")
        
        def suffix(self, suffix: Text.BaseText):
            return CustomCommand(f"team modify {self.name} suffix {suffix}")
        
        def seeFriendlyInvisibles(self, seeFriendlyInvisibles: bool):
            return CustomCommand(f"team modify {self.name} seeFriendlyInvisibles {str(seeFriendlyInvisibles).lower()}")

    @staticmethod
    def modify(name: PartialString):
        return Team._UTeamModifier(name)