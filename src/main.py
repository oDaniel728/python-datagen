from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.fill import Fill
from datagen.function.commands.give import Give
from datagen.function.commands._return import Return
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.commands.setblock import SetBlock
from datagen.function.commands.teleport import Teleport
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.tag.functiontag import FunctionTag
from datagen.tag.tag import Tag
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.blocksettings import BlockSettings
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.position3 import Position3
from datagen.utils.scoreboard.criterion import ObjectiveCriterion

def main():

    dp = DataPack("test_datapack", "DataPack created for testing purposes")
    
    ns = Namespace("test_namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    load_tag = FunctionTag(Identifier.of("minecraft:load"), [])
    mc.add_tag(load_tag)

    hello_world_func = AnonymousFunction(dp)
    hello_world_func += Say("Hello, world!")

    with Function(ns/"test"):
        ~Say("This is a test function.")
        ~Give(TargetSelector.NEAREST_PLAYER, Items.DIAMOND.get_stack(64))

    with Function(ns/"aa"):
        ~SetBlock(BlockPosition(0, 0, 0), Blocks.STONE)
        ~Fill(BlockPosition(1, 0, 0), BlockPosition(3, 0, 0), Blocks.DIRT)
        ~Teleport(TargetSelector.NEAREST_PLAYER, RelativeBlockPosition(0, 10, 0))
        ~TellRaw(TargetSelector.NEAREST_PLAYER, Text.literal("You have been teleported!"))
        ~RunFunction(ns/"test")

    with Function(ns/"scoretest") as scoretest:
        score = Scoreboard.objective("test_score", Text.literal("Test Score"), ObjectiveCriterion.DUMMY)
        ~score.add()
        ~score.set_display("sidebar")
        at_p = TargetSelector.NEAREST_PLAYER
        me = score.player(at_p)
        ~me.set(0)
        ~me.add(25)
        ~me.remove(10)
        ~me.multiply(2)
        ~TellRaw(at_p, Text.BaseText.components(Text.literal("Your score is: "), Text.score(me)))
        ~Return.score(me)

    with Function(ns/"test2"):
        ~Return.function(scoretest)

    load_tag.add_value(hello_world_func)

    dp.build()