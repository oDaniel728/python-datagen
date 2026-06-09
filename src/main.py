from datagen.advancement.advancement import Advancement
from datagen.advancement.criteria import Criteria
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.advancements import Advancements
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.itempredicate import ItemPredicate


def main():
    with DataPack("pack", "a pack") as dp:
        
        with Namespace("pack") as ns:
            
            adv = (
                Advancement(ns / "test").open()
                .set_display(
                    icon = Items.BEDROCK.get_stack(),
                    title = Text.literal("Test Advancement"),
                    description = Text.literal("This is a test advancement"),
                    announce_to_chat=False,
                    show_toast=False,
                    hidden=True
                )
                .set_criteria(
                    Criteria.consume_item(
                        ItemPredicate()
                        .with_items(Items.COOKED_BEEF)
                    )
                )
                .set_rewards(
                    AnonymousFunction(dp)
                    .add_command(Say("You have completed the test advancement!"))
                    .add_command(Advancements.revoke(TargetSelector.SELF, ns / "test"))
                )
                .seal()
            )
            ns.add_advancement(adv)

            with Function(ns / "hello") as f:
                ~ Say("Hello, world!")

        dp.add_namespace(ns)

    dp.build()

#nd