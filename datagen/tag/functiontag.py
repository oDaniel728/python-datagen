from collections.abc import Iterable

from datagen.function.function import Function
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier


class FunctionTag(Tag[Function]):
    def __init__(self, id: Identifier, values: Iterable[Function], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Function