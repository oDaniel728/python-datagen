from typing import Any

from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands._data.datastorage import DataStorage, DataStorageValue
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
    def run(command: Command | CommandArray) -> CommandArray:
        if isinstance(command, CommandArray):
            *cmds, last_command = command.commands
            return CommandArray([*cmds, Return(f"run {last_command.raw()}")])
        else:
            return CommandArray([Return(f"run {command.raw()}")])
    
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
    
    @staticmethod
    def data_storage(storage: "DataStorage", key: str, scale: float | None = None):
        id = storage.id.__str__()
        if scale is not None:
            return Return.run(CustomCommand("data get storage", id, key, str(scale)))
        else:
            return Return.run(CustomCommand("data get storage", id, key))

    def to_string(self) -> str:
        return f"# returns {self.value}\nreturn {self.value}"
    
    def into(self, holder: "DataStorageValue | ScoreboardPlayer") -> Command:
        if isinstance(holder, DataStorageValue):
            return holder.set(self)
        elif isinstance(holder, ScoreboardPlayer):
            return holder.set(self)
        else:
            raise TypeError(f"Cannot return into {type(holder)}")