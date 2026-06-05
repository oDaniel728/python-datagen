from typing import Self

from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.tag.tag import Tag


class Tick(Tag[Function]):
    _instance: Self
    def __new__(cls) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        super().__init__(Namespace.minecraft / "tick", [])
        Namespace.minecraft.add_tag(self)