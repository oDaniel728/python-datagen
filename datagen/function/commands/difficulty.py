from datagen.function.commands.command import Command
from datagen.utils.repr.diff import MCDifficulty


class Difficulty(Command):
    def __init__(self, difficulty: MCDifficulty):
        super().__init__()
        self.difficulty = difficulty

    def __str__(self) -> str:
        return f"difficulty {self.difficulty}"