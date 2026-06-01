from datagen.textcomponents.textcomponent import TextComponent


class ScoreTextComponent(TextComponent):
    def __init__(self, name: str, objective: str) -> None:
        self.name = name
        self.objective = objective

        super().__init__()

    def to_dict(self) -> dict:
        return {
            "type": "score",
            "score": {
                "name": self.name,
                "objective": self.objective,
            },
        }