from datagen.advancement.advancement import Advancement
from datagen.advancement.advancementbuilder import AdvancementBuilder
from datagen.advancement.criteria import Criteria
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.text._components import LiteralText


def main():
    dp = DataPack("test_pack", "This is a test datapack")
    
    ns = Namespace("pack")
    dp += ns
    
    with ~ Function(ns / "test") as test:
        ~ Say("Hello, world!")

    dp.build()
#nd