from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.command import Command
from datagen.function.function import Function
from datagen.types.util.maybe import Maybe
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.repr.placeableblock import PlaceableBlock


class BlockSchematic[B: PlaceableBlock = PlaceableBlock]():
    def __init__(self):
        self.blocks = list[B]()

    def append(self, block: B) -> None:
        self.blocks.append(block)

    def remove(self, block: B) -> None:
        self.blocks.remove(block)

    def __getitem__(self, index: int) -> Maybe[B]:
        if 0 <= index < len(self.blocks):
            return Maybe(self.blocks[index])
        return Maybe(None)
    
    def __len__(self) -> int:
        return len(self.blocks)
    
    def __iter__(self):
        return iter(self.blocks)
    
    def __iadd__(self, other: B) -> "BlockSchematic[B]":
        self.append(other)
        return self
    
    def __isub__(self, other: B) -> "BlockSchematic[B]":
        self.remove(other)
        return self
    
    def __add__[U: PlaceableBlock](self, other: "BlockSchematic[U]") -> "BlockSchematic[U]":
        new_schematic = BlockSchematic[U]()
        for block in self.blocks:
            new_schematic.append(block) # type: ignore
        for block in other.blocks:
            new_schematic.append(block)
        return new_schematic
    
    def __sub__[U: PlaceableBlock](self, other: "BlockSchematic[U]") -> "BlockSchematic[U]":
        new_schematic = BlockSchematic[U]()
        for block in self.blocks:
            if block not in other.blocks:
                new_schematic.append(block) # type: ignore
        return new_schematic
    
    def get_area(self) -> BlockPosition:
        if not self.blocks:
            return BlockPosition(0, 0, 0)
        min_x = min(block.pos.x for block in self.blocks)
        max_x = max(block.pos.x for block in self.blocks)
        min_y = min(block.pos.y for block in self.blocks)
        max_y = max(block.pos.y for block in self.blocks)
        min_z = min(block.pos.z for block in self.blocks)
        max_z = max(block.pos.z for block in self.blocks)
        return BlockPosition(max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1)
    
    def get_start_point(self) -> BlockPosition:
        if not self.blocks:
            return BlockPosition(0, 0, 0)
        min_x = min(block.pos.x for block in self.blocks)
        min_y = min(block.pos.y for block in self.blocks)
        min_z = min(block.pos.z for block in self.blocks)
        return BlockPosition(min_x, min_y, min_z)
    
    def get_end_point(self) -> BlockPosition:
        if not self.blocks:
            return BlockPosition(0, 0, 0)
        max_x = max(block.pos.x for block in self.blocks)
        max_y = max(block.pos.y for block in self.blocks)
        max_z = max(block.pos.z for block in self.blocks)
        return BlockPosition(max_x, max_y, max_z)
    
    def move(self, pos: BlockPosition) -> None:
        for block in self.blocks:
            block.pos.x += pos.x
            block.pos.y += pos.y
            block.pos.z += pos.z

    def copy(self) -> "BlockSchematic[B]":
        new_schematic = BlockSchematic[B]()
        for block in self.blocks:
            new_schematic.append(block) # type: ignore
        return new_schematic

    def place(self, at: BlockPosition) -> list[Command]:
        func = list[Command]()
        for block in self.blocks:
            new_x = block.pos.x + at.x
            new_y = block.pos.y + at.y
            new_z = block.pos.z + at.z
            if isinstance(block.pos, RelativeBlockPosition):
                new_pos = RelativeBlockPosition(new_x, new_y, new_z)
            else:
                new_pos = BlockPosition(new_x, new_y, new_z)
            func.append(block.at(new_pos).place())
        return func