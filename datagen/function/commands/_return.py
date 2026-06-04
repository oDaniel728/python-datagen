from typing import Any
from xml.etree.ElementTree import tostring

from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.function import Function
from datagen.utils.scoreboard.player import ScoreboardPlayer


class Return(Command):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    @staticmethod
    def int(value: int):
        return Return(value)

    @staticmethod
    def run(command: Command):
        return Return(f"run {command.raw()}")
    
    @staticmethod
    def fail():
        return Return("fail")
    
    @staticmethod
    def score(player: ScoreboardPlayer):
        p = player.get().raw()
        return Return.run(CustomCommand(p))
    
    @staticmethod
    def function(function: Function):
        return Return.run(CustomCommand("function", function.id.to_string()))

    def to_string(self) -> str:
        return f"# returns {self.value}\nreturn {self.value}"
    