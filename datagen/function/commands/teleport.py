from typing import Type, overload

from datagen.datapack.datapack import DataPack
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.function import Function
from datagen.globals import DatagenConfig
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3

def may_be_none[T](t: T | Type[T]) -> T:
    return None # type: ignore

class Teleport(Command):

    LOOK_AT_ENTITY: Function[str] = may_be_none(Function[str])

    @overload
    def __init__(self, target: TargetSelector, /) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, destination: TargetSelector, /) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, destination: Position3, /) -> None: ...
    @overload
    def __init__(self, target: TargetSelector, destination: str, /) -> None: ...
    @overload
    def __init__(self, target: str, /) -> None: ...
    @overload
    def __init__(self, target: Position3, /) -> None: ...

    def __init__(self, *args) -> None:
        super().__init__()
        self.target: TargetSelector | Position3 | str
        self.destination: TargetSelector | Position3 | str
        if len(args) == 2:
            t, d = args
            self.target = t
            self.destination = d
        elif len(args) == 1:
            t = args[0]
            self.target = TargetSelector.SELF
            self.destination = t
        else:
            raise Exception("Invalid arguments for Teleport command")

    def to_string(self) -> str:
        target_str = self.target.to_string() if hasattr(self.target, "to_string") else str(self.target) # type: ignore
        destination_str = self.destination.to_string() if hasattr(self.destination, "to_string") else str(self.destination) # type: ignore
        return self.auto_macro(f"tp {target_str} {destination_str}")
    
    @staticmethod
    def look_at_entity(at: TargetSelector | str, /) -> CommandArray:
        if not Teleport.LOOK_AT_ENTITY:
            with DataPack.get_current_datapack().get_namespace_by_name(DatagenConfig.config.get("environmentSettings", {}).get("names", {}).get("namespaces", {}).get("temp", "temp")) as ns:
                with~ Function() as Teleport.LOOK_AT_ENTITY:
                    ~ CustomCommand(f"# Look At Entity {at}")
                    entity = Teleport.LOOK_AT_ENTITY['0']
                    ENTITY = EntityData(f"{entity}")
                    with~ Function() as a1:
                        _0 = a1['0']
                        _1 = a1['1']
                        _2 = a1['2']
                        ~ Teleport.look_at_position(f"{_0} {_1} {_2}")
                    ~ a1.run({
                        "0": ENTITY["Pos"][0], 
                        "1": ENTITY["Pos"][1], 
                        "2": ENTITY["Pos"][2]
                    })
        return Teleport.LOOK_AT_ENTITY.run({"0": f'{at}'})
    
    @staticmethod
    def look_at_position(at: Position3 | str, offset: Position3 | str = '~ ~ ~', /) -> Command:
        return CustomCommand(f"tp @s {offset} facing {at}")