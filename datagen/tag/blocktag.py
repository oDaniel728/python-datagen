from typing import Iterable

from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item


class BlockTag(Tag[Block]):
    r"""
    # BlockTag \: Tag
    - See https://minecraft.wiki/w/Tag_(Java_Edition)
    ## Summary
    Represents a Minecraft block tag, which is a collection of blocks that can be used to group related blocks together. Each block tag has an identifier, a set of blocks, and a flag indicating whether the tag should replace existing tags with the same identifier or merge with them. The BlockTag class provides methods for adding and removing blocks, checking for the presence of blocks, and converting the tag to a JSON representation that can be saved to a file.
    ## Examples
    - Creating a block tag and adding blocks to it
    ```python
    with BlockTag(Identifier.of("pack:example")) as t:
        t += Blocks.COAL_BLOCK
        t += Blocks.IRON_BLOCK
    ```
    """
    def __init__(self, id: Identifier, values: Iterable[Block] = [], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Block