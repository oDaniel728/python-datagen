from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand


class Time():
    _TUnit = Literal["day", "second", "tick"]
    @staticmethod
    def add(time: int, unit: _TUnit = "tick") -> CustomCommand:
        return CustomCommand(f"time add {time} {unit[0]}")
    
    @overload
    @staticmethod
    def set(time: int, unit: _TUnit = "tick", /) -> CustomCommand: ...
    _TTime = Literal["day", "noon", "night", "midnight"]
    @overload
    @staticmethod    
    def set(time: _TTime, /) -> CustomCommand: ...
    
    @staticmethod
    def set(time: int | _TTime, unit: _TUnit = "tick", /) -> CustomCommand:
        if isinstance(time, int):
            return CustomCommand(f"time set {time} {unit[0]}")
        else:
            return CustomCommand(f"time set {time}")
        
    _TQueryTarget = Literal["daytime", "gametime", "day"]
    @staticmethod
    def query(target: _TQueryTarget) -> CustomCommand:
        return CustomCommand(f"time query {target}")