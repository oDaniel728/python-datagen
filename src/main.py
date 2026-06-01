

from collections import namedtuple

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier


def main():
    print("Hello, World!")

    dp = DataPack("example", "An example datapack generated with python-datagen")

    namespace = Namespace("example")
    dp.add_namespace(namespace)
    dp.add_namespace(Namespace.minecraft)
    func = Function(namespace.identifier("func")) \
        .add_command(
            Say("Hello, World!")
        )
    load = Function(namespace.identifier("load")) \
        .add_command(
            RunFunction(func)
        )

    namespace.add(func)
    namespace.add(load)

    load_tag = Tag[Function](namespace.minecraft.identifier("load"), [load])
    Namespace.minecraft.add(load_tag)

    dp.build("generated")