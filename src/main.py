from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.bossbar import BossBar
from datagen.function.commands.execute import Execute
from datagen.function.commands.fill import Fill
from datagen.function.commands.give import Give
from datagen.function.commands._return import Return
from datagen.function.commands.ride import Ride
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
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.position3 import Position3
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagenpp.extras.betterexecute import BetterExecute

def main():

    dp = DataPack("test_datapack", "DataPack created for testing purposes")
    
    ns = Namespace("test_namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    load_tag = FunctionTag(Identifier.of("minecraft:load"), [])
    mc.add_tag(load_tag)

    with Function(ns / "load") as load:
        ~ Say("Hello, world!")
        ~ Return.int(1)

        load_tag.add_value(load)

    with Function(ns / "ride_nearest_cart") as ride_nearest_cart:
        with AnonymousFunction(dp) as lambda1:
            ~ Ride.mount(
                TargetSelector.SELF, 
                TargetSelector.nearest(EntityTypes.MINECART)
            )
            ~ Return.int(1)
            
            with AnonymousFunction(dp) as lambda2:
                ~ Return.int(0)
            
            ~ BetterExecute() \
                .ATAS(TargetSelector.SELF) \
                .CONDITION(
                    lambda b: b.entity(
                        TargetSelector.nearest(EntityTypes.MINECART)
                    ), 
                    Return.function(lambda1),
                    Return.function(lambda2)
                )
            
    with Function(ns / "test_ride_nearest_cart") as test_ride_to_nearest_cart:
        _bossbar = BossBar(ns/"test")
        ~ _bossbar.add()
        ~ Return.function(
            AnonymousFunction(dp)
                .add_commands(
                    Execute()
                        .STORE("result", "bossbar", _bossbar, "value")
                        .RUN(ride_nearest_cart)
                )
        )
    dp.build()