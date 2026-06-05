from typing import Literal

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.collections.slot_ranges import SlotRanges
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item
from datagen.utils.repr.position3 import Position3
from datagen.utils.repr.slot_range import SlotRange


class Loot():
    _THand = Literal["mainhand", "offhand"]
    class _UGenerator():
        def __init__(self, prefix: str) -> None:
            self.prefix = prefix

        def fish(self, loot: Identifier, pos: BlockPosition = RelativeBlockPosition(0, 0, 0), tool: Item | Loot._THand = "mainhand") -> CustomCommand:
            if isinstance(tool, Item):
                _tool = tool.id.to_string()
            else:
                _tool = tool
            return CustomCommand(f"{self.prefix} fish {loot} {pos} {_tool}")
        
        def kill(self, target: TargetSelector) -> CustomCommand:
            return CustomCommand(f"{self.prefix} kill {target}")
        
        def loot(self, loot: Identifier):
            return CustomCommand(f"{self.prefix} loot {loot}")
        
        def mine(self, pos: BlockPosition = RelativeBlockPosition(0, 0, 0), tool: Item | Loot._THand = "mainhand") -> CustomCommand:
            if isinstance(tool, Item):
                _tool = tool.id.to_string()
            else:
                _tool = tool
            return CustomCommand(f"{self.prefix} mine {pos} {_tool}")
    
    class _UReplaceGenerator():
        def __init__(self, prefix: str) -> None:
            self.prefix = prefix

        def block(self, pos: BlockPosition = RelativeBlockPosition(0, 0, 0), slot: SlotRange = SlotRanges.CONTAINER_1) -> Loot._UGenerator:
            return Loot._UGenerator(f"{self.prefix} block {pos} {slot}")
        
        def entity(self, target: TargetSelector, slot: SlotRange = SlotRanges.INVENTORY_1) -> Loot._UGenerator:
            return Loot._UGenerator(f"{self.prefix} entity {target} {slot}")

    @staticmethod
    def give(target: TargetSelector) -> _UGenerator:
        return Loot._UGenerator(f"loot give {target}")
    
    @staticmethod
    def insert(target: BlockPosition) -> _UGenerator:
        return Loot._UGenerator(f"loot insert {target}")

    @staticmethod
    def replace() -> _UReplaceGenerator:
        return Loot._UReplaceGenerator("loot replace")
    
    @staticmethod
    def spawn(pos: Position3) -> _UGenerator:
        return Loot._UGenerator(f"loot spawn {pos}")
    
