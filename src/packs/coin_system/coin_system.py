from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.data import Data
from datagen.function.commands.execute import Execute
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText, ScoreText
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagenpp.extras.packs.pack import Pack


class CoinSystem(Pack, name='csys'):
    def on_prepare(self) -> None:
        return None
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        TAG = "coin"
        SCORE: ScoreboardObjective
        with Function(ns / "load") as load:
            
            SCORE = ~ Scoreboard.objective("coin_healths", LiteralText.EMPTY, ObjectiveCriterion.DUMMY)

            ns += load
            mc.load += load

        with Function(ns / "each_coin") as ec:
            SELF = SCORE.player(TargetSelector.SELF)
            THIS = EntityData(TargetSelector.SELF)
            with AnonymousFunction() as a1:
                ~ THIS["CustomName"].set(f"'{a1["Health"]}'")
                ~ THIS["CustomNameVisible"].set(True)
                tmp += a1
            ~ SELF.set(Data.get("entity", TargetSelector.SELF, "Health"))

            args = DataStorage(tmp / "a1args")
            ~ args["Health"].set(THIS["Health"])
            ~ a1.run(args)

            ns += ec

        with Function(ns / "tick") as tick:
            ~ Execute() \
                .ASAT(
                    TargetSelector
                        .ALL_ENTITIES
                        .with_settings(
                            TargetSelectorSettings()
                            .with_tag(TAG)
                        )
                    ) \
                .RUN(ec)
            
            ns += tick
            mc.tick += tick

    def on_build(self) -> None:
        return None