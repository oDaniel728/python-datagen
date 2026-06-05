from datagen.function.commands.command import Command
from datagen.utils.repr.gamemode import MCGamemode


class Gamemode(Command):
    def __init__(self, gamemode: MCGamemode):
        super().__init__()
        self.gamemode = gamemode

    def to_string(self) -> str:
        return f"gamemode {self.gamemode}"