from json import dumps

from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text

class TellRaw(Command):
    def __init__(self, target: TargetSelector, message: Text.BaseText | list[Text.BaseText]):
        super().__init__()
        self.target = target
        self.message = message

    def to_string(self) -> str:
        return f'tellraw {self.target.to_string()} {dumps([c.to_dict() for c in self.message] if isinstance(self.message, list) else self.message.to_dict())}'