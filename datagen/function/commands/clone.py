from typing import Literal

from datagen.function.commands.command import Command
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier


class Clone(Command):
    _TMode = Literal["replace", "masked", "filtered"]
    _TMask = Literal["normal", "force", "move"]
    def __init__(self, 
        from_: Identifier, 
        pos1: BlockPosition, pos2: BlockPosition, 
        to_: Identifier,
        dest: BlockPosition, 
        mode: _TMode = "replace", 
        mask: _TMask = "normal"
    ):
        super().__init__()
        self.from_ = from_
        self.pos1 = pos1
        self.pos2 = pos2
        self.to_ = to_
        self.dest = dest
        self.mode = mode
        self.mask = mask

    def to_string(self) -> str:
        return f"clone {self.from_} {self.pos1.to_string()} {self.pos2.to_string()} {self.to_} {self.dest.to_string()} {self.mode} {self.mask}"