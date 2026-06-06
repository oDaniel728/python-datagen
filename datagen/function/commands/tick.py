from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.time import Time


class Tick():
    @staticmethod
    def freeze():
        return CustomCommand("tick freeze")
    
    @staticmethod
    def unfreeze():
        return CustomCommand("tick unfreeze")

    @staticmethod
    def query():
        return CustomCommand("tick query")
    
    @staticmethod
    def rate(rate: int):
        return CustomCommand(f"tick rate {rate}")
    
    @overload
    @staticmethod
    def sprint(amount: int, unit: Time._TUnit, /) -> CustomCommand: ...

    @overload
    @staticmethod
    def sprint(value: Literal["stop"], /) -> CustomCommand: ...

    @staticmethod
    def sprint(amount: int | Literal["stop"], unit: Time._TUnit | None = None):
        if unit is not None:
            return CustomCommand(f"tick sprint {amount} {unit}")
        else:
            return CustomCommand(f"tick sprint {amount}")