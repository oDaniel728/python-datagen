from datagen.datapack.namespace import Namespace
from packs.coin_system.pack_objectives.ages import AGES_SOBJ
from packs.coin_system.pack_objectives.coin_healths import COIN_HEALTHS
from packs.coin_system.pack_objectives.roll import ROLL
from packs.coin_system.pack_teams.util import make_rarity_team


class LoadFunction():

    @staticmethod
    def register(ns: Namespace, mc: Namespace) -> None:
        with ns.create_function("load").hook(mc.load) as load:
            ~ COIN_HEALTHS
            ~ AGES_SOBJ
            ~ ROLL

            ~ make_rarity_team("basic")[0]
            ~ make_rarity_team("common")[0]
            ~ make_rarity_team("uncommon")[0]
            ~ make_rarity_team("rare")[0]
            ~ make_rarity_team("epic")[0]
            ~ make_rarity_team("legendary")[0]
