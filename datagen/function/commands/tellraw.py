from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text

class TellRaw(Command):
    def __init__(self, target: TargetSelector, message: Text.BaseText):
        super().__init__()
        self.target = target
        self.message = message

    def to_string(self) -> str:
        return f'tellraw {self.target.to_string()} {self.message.to_string()}'