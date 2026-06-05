from datagen.function.commands.command import Command


class ListPlayers(Command):
    def __init__(self):
        super().__init__()

    def to_string(self) -> str:
        return "list"