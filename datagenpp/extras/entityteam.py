from datagen.function.commands.command import Command
from datagen.function.commands.team import Team
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.obfuscator import Obfuscator

class EntityTeam():
    def __init__(self, name: str, displayname: BaseText = LiteralText.EMPTY):
        self.name = name
        self.displayname = displayname

    def _obf_name(self) -> str:
        return Obfuscator.obfuscate(self.name, "other.entity_teams")

    def add(self) -> Command:
        return Team.add(self._obf_name(), self.displayname)
    
    def join(self, target: TargetSelector) -> Command:
        return Team.join(self._obf_name(), target)
    
    @staticmethod
    def leave(target: TargetSelector) -> Command:
        return Team.leave(target)
    
    def empty(self) -> Command:
        return Team.empty(self._obf_name())
    
    def modify(self) -> Team._UTeamModifier:
        return Team.modify(self._obf_name())
    
    def remove(self) -> Command:
        return Team.remove(self._obf_name())

    def __invert__(self):
        return ~ self.add()