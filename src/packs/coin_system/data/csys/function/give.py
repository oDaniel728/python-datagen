from datagen.datapack.namespace import Namespace
from datagen.function.commands.give import Give
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.extras.item.entityspawnegg import EntitySpawnEgg
from packs.coin_system.pack_entities.coin import Coin


class GiveFunctions():

    @staticmethod
    def register_coin_spawn_egg(ns: Namespace, coin: Coin) -> None:
        with ns.create_function("give/spawn_egg/coin") as give_feather_spawn_egg:
            egg = EntitySpawnEgg(coin)
            ~ Give(TargetSelector.SELF, egg.get_stack())
