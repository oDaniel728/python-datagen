from datagen.datapack.namespace import Namespace
from datagen.function.commands.summon import Summon
from datagen.utils.repr.position3 import Position3
from packs.coin_system.pack_entities.coin import Coin


class SummonFunctions():

    @staticmethod
    def register_coin(ns: Namespace, coin: Coin) -> None:
        with ns.create_function("summon/coins/feather") as summon_feather_coin:
            ~ Summon.entity(coin.type, Position3.auto("~ ~ ~"), coin.nbt())
