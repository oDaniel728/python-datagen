from datagen.datapack.namespace import Namespace
from datagen.extras.packs.pack import Pack
from packs.coin_system.data.csys.enchantment.bundles import BUNDLES
from packs.coin_system.data.csys.enchantment.coins import COINS
from packs.coin_system.data.csys.enchantment.damage import DAMAGE
from packs.coin_system.data.csys.enchantment.emeralds import EMERALDS
from packs.coin_system.data.csys.enchantment.items import ITEMS
from packs.coin_system.data.csys.function.give import GiveFunctions
from packs.coin_system.data.csys.function.load import LoadFunction
from packs.coin_system.data.csys.function.summon import SummonFunctions
from packs.coin_system.data.csys.function.ticks import TickFunctions
from packs.coin_system.data.csys.function.utils import UtilsFunctions
from packs.coin_system.data.csys.loot_table.coins import CoinLootTables
from packs.coin_system.data.csys.tag import COIN_TAG


class CoinSystem(Pack, name='csys'):

    def on_prepare(self) -> None:
        return None

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        ns += BUNDLES, COINS, EMERALDS, DAMAGE, ITEMS

        LoadFunction.register(ns, mc)

        feathercoin = CoinLootTables.register_feather(ns)

        TickFunctions.register(ns, tmp, mc, COIN_TAG)

        GiveFunctions.register_coin_spawn_egg(ns, feathercoin)
        SummonFunctions.register_coin(ns, feathercoin)

        UtilsFunctions.register_run_at_random_position(ns, tmp)

    def on_build(self) -> None:
        return None
