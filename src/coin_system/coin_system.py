from datagen.datapack.namespace import Namespace
from datagen.extras.packs.pack import Pack
from coin_system.data.csys.enchantment.bundles import BUNDLES
from coin_system.data.csys.enchantment.coins import COINS
from coin_system.data.csys.enchantment.damage import DAMAGE
from coin_system.data.csys.enchantment.emeralds import EMERALDS
from coin_system.data.csys.enchantment.items import ITEMS
from coin_system.data.csys.function.give import GiveFunctions
from coin_system.data.csys.function.load import LoadFunction
from coin_system.data.csys.function.summon import SummonFunctions
from coin_system.data.csys.function.ticks import TickFunctions
from coin_system.data.csys.function.utils import UtilsFunctions
from coin_system.data.csys.loot_table.coins import CoinLootTables
from coin_system.data.csys.tag import COIN_TAG


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
