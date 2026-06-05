from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.tag.tag import Tag


class Tick(Tag[Function]):
    def __init__(self):
        super().__init__(Namespace.minecraft / "tick", [])