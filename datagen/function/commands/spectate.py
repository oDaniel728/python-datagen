from datagen.function.commands.command import Command
from datagen.types.exceptions.preventionexception import PreventionException
from datagen.utils.minecraft.targetselector import TargetSelector


class Spectate(Command):
    def __init__(self, who: TargetSelector, to: TargetSelector):
        super().__init__()
        if who == to == TargetSelector.SELF:
            raise PreventionException("Cannot spectate yourself")
        
        self.who, self.to = who, to

    def to_string(self) -> str:
        return f"spectate {self.who} {self.to}"