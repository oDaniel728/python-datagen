from datagen.types.util.holder import Holder


class MCDifficulty(Holder[str]):
    def __init__(self, value: str):
        super().__init__(value)