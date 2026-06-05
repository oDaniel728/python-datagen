from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text


class BossBar():
    def __init__(self, id: Identifier, name: Text.BaseText | str = ""):
        self._id = id
        self._name = name

    def _get_name_string(self) -> str:
        if isinstance(self._name, str):
            return f'"{self._name}"'
        else:
            return self._name.to_string()
    
    def add(self) -> CustomCommand:
        return CustomCommand(f"bossbar add {self._id} {self._get_name_string()}")
    
    _TBossBarGettableProperties = Literal[
        "max",
        "players",
        "value",
        "visible",
    ]
    _TBossBarSettableProperties = Literal[
        "color",
        "name",
        "style",
    ] | _TBossBarGettableProperties
    def get(self, value: _TBossBarGettableProperties = "value") -> CustomCommand:
        return CustomCommand(f"bossbar get {self._id} {value}")
    
    @staticmethod
    def list() -> CustomCommand:
        return CustomCommand("bossbar list")

    @staticmethod
    def remove(id: "Identifier | BossBar") -> CustomCommand:
        return CustomCommand(f"bossbar remove {id if isinstance(id, Identifier) else id._id}")
    
    @overload
    def set(
        self, 
        property: Literal["color"], 
        value: Text.BaseTextSettings.TextColor, 
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["name"],
        value: Text.BaseText | str,
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["style"],
        value: Literal["notched_6", "notched_10", "notched_12", "notched_20", "progress"],
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["max"],
        value: int,
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["players"],
        value: TargetSelector,
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["value"],
        value: int,
        /
    ) -> CustomCommand: ...
    @overload
    def set(
        self,
        property: Literal["visible"],
        value: bool,
        /
    ) -> CustomCommand: ...

    def set(self, property: _TBossBarSettableProperties, value, /) -> CustomCommand:
        if property == "color":
            value_str = value
        elif property == "name":
            value_str = f'"{value}"' if isinstance(value, str) else value.to_string()
        elif property == "style":
            value_str = value
        elif property in ["max", "value"]:
            value_str = str(value)
        elif property == "players":
            value_str = value.to_string()
        elif property == "visible":
            value_str = "true" if value else "false"
        else:
            raise ValueError(f"Invalid property: {property}")
        
        return CustomCommand(f"bossbar set {self._id} {property} {value_str}")
    