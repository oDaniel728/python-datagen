from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.fill import Fill
from datagen.function.commands.give import Give
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.commands.setblock import SetBlock
from datagen.function.commands.teleport import Teleport
from datagen.function.function import Function
from datagen.tag.tag import Tag
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.blocksettings import BlockSettings
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3

def main():
    print("Hello, World!")

    dp = DataPack("example", "An example datapack generated with python-datagen")

    namespace = Namespace("example")
    dp.add_namespace(namespace)
    dp.add_namespace(Namespace.minecraft)
    func = Function(namespace.identifier("func")) \
        .add_commands(
            Say("Hello, World!"),
            Fill(
                BlockPosition(0, 0, 0), 
                BlockPosition(10, 10, 10), 
                Blocks.OAK_LOG.with_settings(BlockSettings.LOGS(axis="y"))
            ),
            SetBlock(RelativeBlockPosition(0, -1, 0), Blocks.DIAMOND_BLOCK),
            Give(TargetSelector.SELF, Items.DIAMOND.get_stack(64)),
            Teleport(Position3(1, 2, 3)),
            RunFunction(
                AnonymousFunction(dp) \
                    .add_command(
                        Say("Anonymous function")
                    )
                )
        )
    load = Function(namespace.identifier("load")) \
        .add_command(
            RunFunction(func)
        )

    namespace.add(func)
    namespace.add(load)

    load_tag = Tag[Function](namespace.minecraft.identifier("load"), [load])
    Namespace.minecraft.add(load_tag)

    dp.build()