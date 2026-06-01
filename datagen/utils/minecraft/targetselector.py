from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings


class TargetSelector():

    NEAREST_PLAYER: TargetSelector
    NEAREST_ENTITY: TargetSelector

    ALL_ENTITIES: TargetSelector
    ALL_PLAYERS: TargetSelector

    RANDOM_PLAYER: TargetSelector
    RANDOM_ENTITY: TargetSelector

    def __init__(self, _value: str, filters: dict | TargetSelectorSettings = {}) -> None:
        self._value = _value
        self.filters = filters if isinstance(filters, dict) else filters.to_dict()

    def __str__(self) -> str:
        if not self.filters:
            return self._value
        return f"{self._value}[{','.join(f'{k}={v}' for k, v in self.filters.items() if not v is None)}]"
    
    def __invert__(self):
        return self.__str__()

TargetSelector.NEAREST_PLAYER = TargetSelector("@p")
TargetSelector.NEAREST_ENTITY = TargetSelector("@e", TargetSelectorSettings(sort="nearest", limit=1))

TargetSelector.ALL_ENTITIES = TargetSelector("@e")
TargetSelector.ALL_PLAYERS = TargetSelector("@a")

TargetSelector.RANDOM_PLAYER = TargetSelector("@r")
TargetSelector.RANDOM_ENTITY = TargetSelector("@e", TargetSelectorSettings(sort="random", limit=1))