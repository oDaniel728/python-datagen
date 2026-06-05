from datagen.function.commands.command import Command
from datagen.utils.repr.gamemode import MCGamemode


class Publish(Command):
    def __init__(self, cheats: bool, gamemode: MCGamemode, port: int = 8080):
        super().__init__()

        self.cheats = cheats
        self.gamemode = gamemode
        self.port = port

    def to_string(self) -> str:
        return f"public {"true" if self.cheats else "false"} {self.gamemode} {self.port}"