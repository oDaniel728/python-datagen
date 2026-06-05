from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector


class Kill(Command):
    def __init__(self, target: TargetSelector):
        super().__init__()

        self.target = target

    def to_string(self) -> str:
        return f"kill {self.target}"