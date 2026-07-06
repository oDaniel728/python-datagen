from typing import Literal

from datagen.extras.repr.entity import Entity
from datagen.function.commands.command import Command
from datagen.function.function import Function
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class CommandChain():
    _last = Function.current_function
    _TMode = Literal["single"]
    def __init__(self, mode: _TMode = "single") -> None:
        self.commands: list[Command] = []
        self.mode = mode

    def add_command(self, command: Command):
        self.commands.append(command)

    def __enter__(self):
        self._last = Function.current_function # type: ignore
        Function.current_function = self # type: ignore
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        Function.current_function = self._last # type: ignore

    def entity(self) -> Entity:
        props = dict()
        
        if self.mode == "single":
            props = {
                "Time": 1,
                "BlockState": {"Name": "minecraft:redstone_block"},
                "Passengers": [
                    {"id": "minecraft:falling_block", "Time": 1, "BlockState": {"Name": "minecraft:activator_rail"}, "Passengers": [
                        {"id": "minecraft:command_block_minecart", "Command": f"{command.raw()}"}
                        for command in self.commands
                    ]},
                    {"id": "minecraft:command_block_minecart", "Command": f'setblock ~ ~1 ~ command_block{{auto:1,Command:"fill ~ ~ ~ ~ ~-{len(self.commands) - 1} ~ air"}}'},
                    {"id": "minecraft:command_block_minecart", "Command": 'kill @e[type=command_block_minecart,distance=..1]'}
                ]
            }

        return Entity(EntityTypes.FALLING_BLOCK, props)