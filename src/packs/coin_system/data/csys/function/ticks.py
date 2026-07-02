from datagen.entitytag import EntityTag
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands import tag
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.clear import Clear
from datagen.function.commands.data import Data
from datagen.function.commands.execute import Execute
from datagen.function.commands.random import Random
from datagen.function.commands.team import Team
from datagen.function.function import Function
from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagen.extras.item.settings.baseitemsettings import BaseItemSettings
from packs.coin_system.pack_objectives.ages import AGES_SOBJ
from packs.coin_system.pack_objectives.coin_healths import COIN_HEALTHS
from packs.coin_system.pack_objectives.roll import ROLL
from packs.coin_system.pack_selectors.glowing_items import NOT_GLOWING_ITEMS
from packs.coin_system.pack_selectors.orbs import EXP_ORB
from packs.coin_system.pack_settings import textsettings


class TickFunctions():

    @staticmethod
    def register(ns, tmp, mc, coin_tag: EntityTag) -> None:
        each_coin = TickFunctions._register_each_coin(ns, tmp, mc)
        TickFunctions._register_main_tick(ns, mc, each_coin, coin_tag)
        TickFunctions._register_clear_bundles(ns, mc)
        TickFunctions._register_add_tag_glow(ns, tmp, mc)
        TickFunctions._register_make_items_glow(ns, mc)
        TickFunctions._register_each_coin_item(ns, tmp, mc)
        TickFunctions._register_each_exp_orb(ns, tmp, mc)

    @staticmethod
    def _register_each_coin(ns, tmp, mc) -> Function:
        with ns.create_function("ticks/each_coin").hook(mc.tick) as ec:
            SSELF = COIN_HEALTHS.player(TargetSelector.SELF)
            DSELF = EntityData(TargetSelector.SELF)

            with AnonymousFunction() as a1:
                ~ DSELF["CustomName"].set(f"'{a1["Health"]}'")
                ~ DSELF["CustomNameVisible"].set(True)
                tmp += a1
            ~ SSELF.set(Data.get("entity", TargetSelector.SELF, "Health"))

            args = DataStorage(tmp / "a1args")
            ~ args["Health"].set(DSELF["Health"])
            ~ a1.run(args)
        return ec

    @staticmethod
    def _register_main_tick(ns, mc, each_coin: Function, coin_tag: EntityTag) -> None:
        with ns.create_function("tick").hook(mc.tick) as tick:
            ~ Execute() \
                .ASAT(
                    TargetSelector
                        .ALL_ENTITIES
                        .with_settings(
                            TargetSelectorSettings()
                            .with_tag(coin_tag)
                        )
                    ) \
                .RUN(each_coin)

    @staticmethod
    def _register_clear_bundles(ns, mc) -> None:
        with ns.create_function("ticks/clear_bundles").hook(mc.tick) as clear_bundles:
            ~ Clear(TargetSelector.ALL_PLAYERS, Items.BUNDLE.with_settings(
                BaseItemSettings().with_custom_data({"bundle": True}).with_("bundle_contents", "[]")
            ))

    @staticmethod
    def _register_add_tag_glow(ns, tmp, mc) -> None:
        with ns.create_function("ticks/add_tag_glow").hook(mc.tick) as add_tag_glow:
            with ns.create_function("ticks/inner/add_tag_glow") as inner_add_tag_glow:
                DSELF = EntityData(TargetSelector.SELF)
                SSELF = AGES_SOBJ.player(TargetSelector.SELF)
                ~ SSELF.set(DSELF["Age"].get())
                ~ tag._Tag.add("glow", NOT_GLOWING_ITEMS)

            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_tag("!glow")
                    )
                ) \
                .RUN(inner_add_tag_glow)

    @staticmethod
    def _register_make_items_glow(ns, mc) -> None:
        with ns.create_function("ticks/make_items_glow").hook(mc.tick) as make_items_glow:
            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_tag("glow")
                    )
                ) \
                .RUN(
                    EntityData(TargetSelector.SELF)["Glowing"].set(True)
                )

    @staticmethod
    def _register_each_coin_item(ns, tmp, mc) -> None:
        with ns.create_function("ticks/each_coin_item").hook(mc.tick) as each_coin_item:
            with ns.create_function("ticks/inner/each_coin_item") as each_item:
                DSELF = EntityData(TargetSelector.SELF)

                SSELF = ROLL.player(TargetSelector.SELF)
                ~ SSELF.set(Random.value(Range(1, 250)))

                ~ DSELF["CustomNameVisible"].set(True)

                with AnonymousFunction() as _:
                    item_name = _['0']
                    count = _['1']
                    id = _['2']
                    rarity = _['3']
                    ~ DSELF["CustomName"].set(f"[{{ \"text\": \"{count}x \" }}, {item_name}]")
                    ~ Team.join(rarity, TargetSelector.SELF)
                    tmp += _

                ~ _.run({
                    "0": DSELF["Item"]["components"]["minecraft:item_name"],
                    "1": DSELF["Item"]["count"],
                    "2": DSELF["Item"]["id"],
                    "3": DSELF["Item"]["components"]["minecraft:custom_data"]["rarity"]
                })
                ~ Execute() \
                    .IF(lambda b: b.score(SSELF, "matches", Range(1, 2))) \
                    .RUN(DSELF["Motion[1]"].set(0.2))

            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_nbt({"Item": {"components": {"minecraft:custom_data": {"show": True}}}})
                    )
                ) \
                .RUN(each_item)

    @staticmethod
    def _register_each_exp_orb(ns, tmp, mc) -> None:
        with ns.create_function("ticks/each_exp_orb").hook(mc.tick) as each_exp_orb:
            with ns.create_function("ticks/inner/each_exp_orb") as each_orb:
                DSELF = EntityData(TargetSelector.SELF)
                with AnonymousFunction() as a2:
                    ~ DSELF["CustomNameVisible"].set(True)
                    ~ DSELF["CustomName"].set(
                        LiteralText(f"{a2['Value']}", textsettings.RARE)
                    )

                    SSELF = ROLL.player(TargetSelector.SELF)
                    ~ SSELF.set(Random.value(Range(1, 250)))
                    ~ Execute() \
                        .IF(lambda b: b.score(SSELF, "matches", Range(1, 2))) \
                        .RUN(DSELF["Motion"][1].set(0.2))

                    tmp += a2
                ARGS = DataStorage(tmp / "a2args")
                ~ ARGS["Value"].set(DSELF["Value"].get(1))
                ~ a2.run(ARGS)

            ~ Execute() \
                .ASAT(EXP_ORB) \
                .RUN(each_orb)
