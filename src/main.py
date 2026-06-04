from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
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

def main():

    dp = DataPack("test_datapack", "DataPack created for testing purposes")
    
    ns = Namespace("test_namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    load_tag = FunctionTag(Identifier.of("minecraft:load"), [])
    mc.add_tag(load_tag)

    with Function(ns / "load") as this:
        ~ Say("Hello, world!")
        ~ Return.int(1)

        load_tag.add_value(this)

    with Function(ns / "ride_nearest_cart") as this:
        with AnonymousFunction(dp) as anon:
            ~ Ride.mount(
                TargetSelector.SELF, 
                TargetSelector.nearest(EntityTypes.MINECART)
            )
            this += RunFunction(anon)
        
        ~ Return.int(1)

    dp.build()