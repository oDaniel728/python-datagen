from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector


class Ride():
    @staticmethod
    def mount(
        rider: TargetSelector, 
        mount: TargetSelector
    ) -> CustomCommand:
        return CustomCommand(f"ride {rider} mount {mount}")
    
    @staticmethod
    def dismount(
        rider: TargetSelector, 
        mount: TargetSelector
    ) -> CustomCommand:
        return CustomCommand(f"ride {rider} dismount {mount}")