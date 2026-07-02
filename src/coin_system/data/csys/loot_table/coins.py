from datagen.datapack.namespace import Namespace
from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.levelbasedvalue import LevelBasedValues
from coin_system.pack_entities.coin import Coin
from coin_system.pack_items.coinbundleitem import CoinBundleItem, ItemBundle
from coin_system.pack_items.coins.feather import FeatherCoin
from coin_system.pack_loot.coinloot import CoinLoot
from coin_system.pack_settings import textsettings


class CoinLootTables():

    @staticmethod
    def register_feather(ns: Namespace) -> Coin:
        feathercoinloot = CoinLoot(ns / "coin_tables/coin") \
            .add_coin_with_bonus(
                FeatherCoin(),
                Range(1, 3),
                Range(1, 10),
                weight=1,
                unenchanted_chance=0.1,
                enchanted_chance=LevelBasedValues.linear(0.1, 0.09)
            ) \
            .add_bundle(
                CoinBundleItem(
                    FeatherCoin(), 10, LiteralText("Coin Bundle I", textsettings.COMMON), "common"
                ),
                unenchanted_chance=0.2,
                enchanted_chance=LevelBasedValues.lookup([i / 10 for i in range(1, 6)], 0)
            ) \
            .add_bundle(
                CoinBundleItem(
                    FeatherCoin(), 25, LiteralText("Coin Bundle II", textsettings.UNCOMMON), "uncommon"
                ),
                unenchanted_chance=0.1,
                enchanted_chance=LevelBasedValues.lookup([max(0, i / 5) for i in range(-4, 7)], 0)
            ) \
            .add_bundle(
                ItemBundle(
                    [FeatherCoin().get_stack(25)] * 4,
                    LiteralText("Coin Bundle III", textsettings.RARE),
                    "rare"
                ),
                unenchanted_chance=0.005,
                enchanted_chance=LevelBasedValues.lookup([max(0, i / 2) for i in range(-8, 3)], 0)
            ) \
            .seal()
        ns += feathercoinloot
        feathercoin = Coin(
            EntityTypes.CHICKEN,
            feathercoinloot
        )
        return feathercoin
