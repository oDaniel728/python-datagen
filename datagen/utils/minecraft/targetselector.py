from typing import Any, Iterable

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.entitytype import EntityType

class TargetSelector():

    SELF: TargetSelector

    NEAREST_PLAYER: TargetSelector
    NEAREST_ENTITY: TargetSelector

    ALL_ENTITIES: TargetSelector
    ALL_PLAYERS: TargetSelector

    RANDOM_PLAYER: TargetSelector
    RANDOM_ENTITY: TargetSelector

    def __init__(self, _value: str, filters: "dict | TargetSelectorSettings" = {}) -> None:
        self._value = _value
        self.filters = filters if isinstance(filters, dict) else filters.to_dict()

    def with_settings(self, filters: "dict | TargetSelectorSettings" = {}):
        _filters = filters if isinstance(filters, dict) else filters.to_dict()
        return TargetSelector(self._value, { **self.filters, **_filters })

    def __format(self, data: Any, d: int = 0) -> Any:
        if isinstance(data, Identifier):
            return ~data
        elif isinstance(data, (list, tuple, set)):
            data = [ self.__format(i, d + 1) for i in data ]
        elif isinstance(data, dict):
            data = { 
                self.__format(k, d + 1): self.__format(v, d + 1) 
                for k, v in data.items()
            }
        elif hasattr(data, "to_dict") and callable(data.to_dict):
            return data.to_dict()
        elif hasattr(data, "to_string") and callable(data.to_string):
            return data.to_string()
        
        return data

    def __str__(self) -> str:
        if not self.filters:
            return self._value
        return f"{self._value}[{','.join(f'{k}={v}' for k, v in self.__format(self.filters).items() if not v is None)}]" \
         .replace(", 'components': {}", "")
    
    def __invert__(self):
        return self.__str__()
    
    def to_string(self): return ~self

    @staticmethod
    def nearest(entity: EntityType, limit: int = 1, filters: dict | TargetSelectorSettings = {}) -> "TargetSelector":
        return TargetSelector("@e", TargetSelectorSettings(type=entity, **filters if isinstance(filters, dict) else filters.to_dict(), sort="nearest", limit=limit))

    @staticmethod
    def furthest(entity: EntityType, limit: int = 1, filters: dict | TargetSelectorSettings = {}) -> "TargetSelector":
        return TargetSelector("@e", TargetSelectorSettings(type=entity, **filters if isinstance(filters, dict) else filters.to_dict(), sort="furthest", limit=limit))

    @staticmethod
    def random(entity: EntityType, limit: int = 1, filters: dict | TargetSelectorSettings = {}) -> "TargetSelector":
        return TargetSelector("@e", TargetSelectorSettings(type=entity, **filters if isinstance(filters, dict) else filters.to_dict(), sort="random", limit=limit))

    @staticmethod
    def arbitrary(entity: EntityType, limit: int = 1, filters: dict | TargetSelectorSettings = {}) -> "TargetSelector":
        return TargetSelector("@e", TargetSelectorSettings(type=entity, **filters if isinstance(filters, dict) else filters.to_dict(), sort="arbitrary", limit=limit))

TargetSelector.SELF = TargetSelector("@s")

TargetSelector.NEAREST_PLAYER = TargetSelector("@p")
TargetSelector.NEAREST_ENTITY = TargetSelector("@e", TargetSelectorSettings(sort="nearest", limit=1))

TargetSelector.ALL_ENTITIES = TargetSelector("@e")
TargetSelector.ALL_PLAYERS = TargetSelector("@a")

TargetSelector.RANDOM_PLAYER = TargetSelector("@r")
TargetSelector.RANDOM_ENTITY = TargetSelector("@e", TargetSelectorSettings(sort="random", limit=1))