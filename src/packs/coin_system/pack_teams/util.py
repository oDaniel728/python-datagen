from datagen.function.commands.commandarray import CommandArray
from datagen.types.literals.textcolor import TextColor
from datagen.utils.minecraft.text._components import LiteralText
from datagen.entityteam import EntityTeam
from packs.coin_system.pack_items.coinitem import CoinItem

def make_team(name: str, color: TextColor, display_name: str = '') -> tuple[CommandArray, EntityTeam]:
    arr = CommandArray([])
    team = EntityTeam(name, LiteralText(display_name))
    arr += team.add()
    arr += team.modify().color(color)
    return arr, team

def make_rarity_team(name: CoinItem._TRarity) -> tuple[CommandArray, EntityTeam]:
    arr = CommandArray([])
    team = EntityTeam(name, LiteralText(name.capitalize()))
    arr += team.add()
    arr += team.modify().color(CoinItem.get_rarity_map()[name].color)
    return arr, team