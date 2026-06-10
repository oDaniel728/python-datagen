from datagen.advancement.advancement import Advancement
from datagen.advancement.criteria import Criteria
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.advancements import Advancements
from datagen.function.commands.give import Give
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.itempredicate import ItemPredicate
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder
from packitems import StickFood

def main():
    with DataPack("pack", "a pack") as dp:
        
        with Namespace("pack") as ns:

            with Function(ns / "on_consume_of_stick") as f:
                ~ Say("You consumed a stick!")

            ~ ScriptBuilder().on_criteria(
                Criteria.consume_item(
                    ItemPredicate()
                    .with_items(Items.STICK)
                ), f
            )

            with Function(ns / "hello") as f:
                ~ Say("Hello, world!")

            with Function(ns / "give_stick") as f:
                ~ Give(
                    TargetSelector.SELF,
                    StickFood().get_stack()
                )

        dp.add_namespace(ns)

    dp.build()

#nd