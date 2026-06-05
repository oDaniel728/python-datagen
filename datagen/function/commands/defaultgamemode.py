from datagen.function.commands.command import Command
from datagen.utils.repr.gamemode import MCGamemode


class DefaultGamemode(Command):
    def __init__(self, gamemode: MCGamemode):
        super().__init__()
        self.gamemode = gamemode

    def to_string(self) -> str:
        return f"defaultgamemode {self.gamemode}"