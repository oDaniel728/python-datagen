from collections.abc import Iterable

from datagen.function.function import Function
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier


class FunctionTag(Tag[Function]):
    r"""
    # FunctionTag \: Tag
    - See https://minecraft.wiki/w/Tag_(Java_Edition)
    ## Summary
    Represents a Minecraft function tag, which is a collection of functions that can be used to group related functions together. Each function tag has an identifier, a set of functions, and a flag indicating whether the tag should replace existing tags with the same identifier or merge with them. The FunctionTag class provides methods for adding and removing functions, checking for the presence of functions, and converting the tag to a JSON representation that can be saved to a file.
    ## Examples
    - Creating a function tag and adding functions to it
    ```python
    with FunctionTag(Identifier.of("pack:example")) as t:
        t += ...
    ```
    """
    def __init__(self, id: Identifier, values: Iterable[Function], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Function