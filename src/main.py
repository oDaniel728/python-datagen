from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function


def main():
    with DataPack("pack", "a pack") as dp:
        
        with Namespace("pack") as ns:
            
            with Function(ns / "hello") as f:
                ~ Say("Hello, world!")

        dp.add_namespace(ns)

    dp.build()

#nd