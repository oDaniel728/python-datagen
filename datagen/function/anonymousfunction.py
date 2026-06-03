from typing import Self
from uuid import uuid4

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class AnonymousFunction(Function):

    def __init__(self, datapack: DataPack):
        super().__init__(Namespace.temp.identifier(f"fun{len(Namespace.temp.functions)}"))
        self.datapack = datapack
        self.datapack.add_namespace(Namespace.temp)
        Namespace.temp.add(self)