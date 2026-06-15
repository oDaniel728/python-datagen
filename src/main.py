from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function


def main():
    dp = DataPack("enchantment_demo", "Demonstrating custom enchantments")
    ns = Namespace("demo")
    dp += ns

    with ~ Function(ns / "hello") as hello:
        ~ Say("Hello world!")

    dp.build()


main()

#nd