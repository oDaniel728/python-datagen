from datagen.function.commands.customcommand import CustomCommand
from datagen.types.util.min import Range


class Random():
    @staticmethod
    def value(range: Range | str) -> CustomCommand:
        return CustomCommand(f"random value {range}")