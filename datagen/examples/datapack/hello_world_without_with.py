from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function

def main():
    dp = DataPack("pack", "a pack")
    ns = Namespace("pack")
    f = Function(ns / "hello")
    f.add_command(Say("Hello, world!"))
    dp.add_namespace(ns)
    dp.build()