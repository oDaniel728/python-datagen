from abc import ABC

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.logger import Logger


class Pack(ABC):
    # class SomePack(Pack, name: str, description: str = '')
    def __init_subclass__(cls, name: str, description: str = '') -> None:
        cls.dp = DataPack(name, description)

    def __init__(self):
        self.dp  : DataPack
        self.logger: Logger
        self.ns  : Namespace
        self.mc  : Namespace
        self.tmp : Namespace
        self.__prepare__()
        self.__register__()
        self.__build__()

    def __repr__(self) -> str:
        return f"Pack(name={self.dp.name}, ...)"

    def __prepare__(self):
        self.ns = Namespace(self.dp.name.lower())
        self.mc = Namespace.minecraft()
        self.tmp = Namespace.temp()
        self.logger = Logger(self.dp.name)
        self.on_prepare()

    def __register__(self):
        self.dp += self.ns, self.mc, self.tmp
        self.on_register(self.ns, self.mc, self.tmp)

    def __build__(self):
        self.dp.build()
        self.on_build()

    def on_prepare(self) -> None:
        pass

    def on_register(
        self, 
        ns: Namespace, 
        mc: Namespace, 
        tmp: Namespace
    ) -> None:
        pass

    def on_build(self) -> None:
        pass