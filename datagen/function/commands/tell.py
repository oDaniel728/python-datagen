from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector


class Tell(Command):
    def __init__(self, target: TargetSelector, message: str):
        self.target = target
        self.message = message

    def to_string(self) -> str:
        return f'tell {self.target} {self.message}'