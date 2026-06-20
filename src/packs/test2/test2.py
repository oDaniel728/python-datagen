from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function
from packs.tests.tests import Tests


class Test2():

    def __init__(self) -> None:
        self.dp = DataPack("test2", "")
        self.ns : Namespace
        self.mc : Namespace
        self.tmp: Namespace
        
        self.prepare()
        self.register()
        self.build()

    def prepare(self) -> None: 
        self.ns = Namespace(self.dp.name)
        self.mc = Namespace.minecraft()
        self.tmp = Namespace.temp()

    def register(self) -> None: 
        self.dp += self.ns, self.mc, self.tmp
        ns, mc, tmp = self.ns, self.mc, self.tmp

        with~ Function(ns / "func") as lmain:
            i = lmain['i']
            min = lmain['min']
            max = lmain['max']
            step = lmain['step']
            ~ Say(f"Iteração {i} em {min}..{max} com passo {step}")
        
        with~ Function(ns / "load"):
            ~ Tests.loopStart(1, 10, 1, lmain)


    def build(self) -> None:
        self.dp.build()
