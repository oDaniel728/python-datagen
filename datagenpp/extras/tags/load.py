from typing import Self

from datagen.datapack.namespace import Namespace
from datagen.tag.functiontag import FunctionTag


class Load(FunctionTag):

    _instance: Self
    def __new__(cls) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__(Namespace.minecraft / "load", [])
        Namespace.minecraft.add_tag(self)