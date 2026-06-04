#type: ignore
from typing import Self
from uuid import uuid4

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class AnonymousFunction(Function):

    def __new__(cls, datapack: DataPack) -> Self:
        id = Namespace.temp.identifier(f"fun{len(Namespace.temp.functions)}")
        if id in cls._Function__funcs:
            return cls._Function__funcs[id]
        else:
            func = super(AnonymousFunction, cls).__new__(cls, id)
            cls._Function__funcs[id] = func
            return func

    def __init__(self, datapack: DataPack):
        super().__init__(Namespace.temp.identifier(f"fun{len(Namespace.temp.functions)}"))
        self.datapack = datapack
        self.datapack.add_namespace(Namespace.temp)
        Namespace.temp.add(self)