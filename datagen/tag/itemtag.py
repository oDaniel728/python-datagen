from typing import Iterable

from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item


class ItemTag(Tag[Item]):
    r"""
    # ItemTag \: Tag
    - See https://minecraft.wiki/w/Tag_(Java_Edition)
    ## Summary
    Represents a Minecraft item tag, which is a collection of items that can be used to group related items together. Each item tag has an identifier, a set of items, and a flag indicating whether the tag should replace existing tags with the same identifier or merge with them. The ItemTag class provides methods for adding and removing items, checking for the presence of items, and converting the tag to a JSON representation that can be saved to a file.
    ## Examples
    - Creating an item tag and adding items to it
    ```python
    with ItemTag(Identifier.of("pack:example")) as t:
        t += Items.COAL
        t += Items.IRON_INGOT
    ```
    """
    def __init__(self, id: Identifier, values: Iterable[Item] = [], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Item