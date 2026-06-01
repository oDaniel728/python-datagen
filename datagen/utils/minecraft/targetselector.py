class TargetSelector():

    NEAREST_PLAYER: TargetSelector
    NEAREST_ENTITY: TargetSelector

    ALL_ENTITIES: TargetSelector
    ALL_PLAYERS: TargetSelector

    RANDOM_PLAYER: TargetSelector
    RANDOM_ENTITY: TargetSelector

    def __init__(self, _value: str, filters: dict) -> None:
        self._value = _value
        self.filters = filters

TargetSelector.NEAREST_PLAYER = TargetSelector("@p", {})
TargetSelector.NEAREST_ENTITY = TargetSelector("@e", {"sort": "nearest", "limit": 1})
