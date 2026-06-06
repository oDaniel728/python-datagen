from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.targetselector import TargetSelector


class _Tag():
    @staticmethod
    def add(name: str, target: TargetSelector):
        return CustomCommand(f"tag {target} add {name}")
    @staticmethod
    def list(target: TargetSelector):
        return CustomCommand(f"tag {target} list")
    @staticmethod
    def remove(name: str, target: TargetSelector):
        return CustomCommand(f"tag {target} remove {name}")