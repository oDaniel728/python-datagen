from datagen.function.commands.command import Command
from datagen.function.commands.tag import _Tag
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.obfuscator import Obfuscator


class EntityTag():
    def __init__(self, name: str) -> None:
        self.name = name

    def _obf_name(self) -> str:
        return Obfuscator.obfuscate(self.name, "other.entity_tags")

    def add(self, target: TargetSelector) -> Command:
        return _Tag.add(self._obf_name(), target)

    def remove(self, target: TargetSelector) -> Command:
        return _Tag.remove(self._obf_name(), target)

    @staticmethod
    def list(target: TargetSelector) -> Command:
        return _Tag.list(target)
    
    def __str__(self) -> str:
        return self.name