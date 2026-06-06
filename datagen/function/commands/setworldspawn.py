from datagen.function.commands.command import Command
from datagen.utils.repr.position3 import Position3


class SetWorldSpawn(Command):
    def __init__(self, pos: Position3):
        super().__init__()
        self.pos = pos

    def to_string(self) -> str:
        return f"setworldspawn {self.pos.x} {self.pos.y} {self.pos.z}"