from datagen.function.commands.command import Command
from datagen.function.commands.tag import _Tag
from datagen.utils.minecraft.targetselector import TargetSelector


class EntityTag():
    def __init__(self, name: str) -> None:
        self.name = name
    
    def add(self, target: TargetSelector) -> Command:
        return _Tag.add(self.name, target)

    def remove(self, target: TargetSelector) -> Command:
        return _Tag.remove(self.name, target)

    @staticmethod
    def list(target: TargetSelector) -> Command:
        return _Tag.list(target)