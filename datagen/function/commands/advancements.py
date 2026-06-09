from datagen.advancement.advancement import Advancement
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector


class Advancements():
    @staticmethod
    def grant(player: TargetSelector, advancement: Identifier | Advancement):
        return CustomCommand("advancement", "grant", player.to_string(), "only", ~(advancement.id if isinstance(advancement, Advancement) else advancement))

    @staticmethod
    def revoke(player: TargetSelector, advancement: Identifier | Advancement):
        return CustomCommand("advancement", "revoke", player.to_string(), "only", ~(advancement.id if isinstance(advancement, Advancement) else advancement))