from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3


class SpawnPoint(Command):
    def __init__(self, pos: Position3):
        super().__init__()
        self.pos = pos

    def apply_to(self, target: TargetSelector) -> CustomCommand:
        return CustomCommand(f"spawnpoint {target} {self.pos}")

    def to_string(self) -> str:
        return f"spawnpoint @a {self.pos.x} {self.pos.y} {self.pos.z}"