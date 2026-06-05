from typing import overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.repr.biome import Biome


class FillBiome(Command):
    @overload
    def __init__(self,
        fromPos: BlockPosition,
        toPos: BlockPosition,
        biome: Biome,
        /,
    ) -> None: ...
    @overload
    def __init__(self,
        fromPos: BlockPosition,
        toPos: BlockPosition,
        biome: Biome,
        replace: bool,
        biomeToReplace: Biome,
        /,
    ) -> None: ...
    
    def __init__(self,
        fromPos: BlockPosition,
        toPos: BlockPosition,
        biome: Biome,
        replace: bool | None = None,
        biomeToReplace: Biome | None = None,
        /,
    ) -> None: 
        super().__init__()

        self.fromPos = fromPos
        self.toPos = toPos
        self.biome = biome
        self.replace = replace
        self.biomeToReplace = biomeToReplace

    def to_string(self) -> str:
        if self.replace != None and self.biomeToReplace != None:
            return f"fillbiome {self.fromPos} {self.toPos} {self.biome} replace {self.biomeToReplace}"
        else:
            return f"fillbiome {self.fromPos} {self.toPos} {self.biome}"