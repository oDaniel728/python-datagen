from abc import ABC, abstractmethod

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace


class Pack(ABC):
    def __init__(self, dp: DataPack) -> None:
        self.dp = dp
        self.ns : Namespace
        self.mc : Namespace

        self.prepare()
        self.register()
        self.build()


    def prepare(self) -> None:
        self.ns = Namespace(self.dp.name)
        self.mc = Namespace.minecraft()

    @abstractmethod
    def register(self) -> None: ...
    
    def build(self) -> None: 
        self.dp.build()