from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.position3 import Position3

class SpreadPlayers():
    @staticmethod
    def spread(
        center: Position3,
        spread_distance: float,
        max_range: float,
        respect_teams: bool,
        targets: TargetSelector
    ) -> Command:
        return CustomCommand(f"spreadplayers {center} {spread_distance} {max_range} {'respectTeams' if respect_teams else 'underlying'} {targets}")

    @staticmethod
    def under(
        center: Position3,
        spread_distance: float,
        max_range: float,
        respect_teams: bool,
        targets: TargetSelector,
        height: int
    ) -> Command:
        return CustomCommand(f"spreadplayers {center} {spread_distance} {max_range} {'respectTeams' if respect_teams else 'underlying'} {targets} under {height}")