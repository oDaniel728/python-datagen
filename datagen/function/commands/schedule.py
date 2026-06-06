from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.time import Time
from datagen.function.function import Function


class Schedule():
    @staticmethod
    def clear(func: Function) -> CustomCommand:
        return CustomCommand(f"schedule clear {func.id}")
    
    @staticmethod
    def function(
        func: Function,
        delay: int, unit: Time._TUnit,
        mode: Literal["append", "replace"] = "append"
    ) -> CustomCommand:
        return CustomCommand(f"schedule function {func.id} {delay} {unit} {mode}")