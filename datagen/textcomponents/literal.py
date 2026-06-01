from datagen.textcomponents.textcomponent import TextComponent
from datagen.textcomponents.textcomponentsettings import TextComponentSettings


class LiteralTextComponent(TextComponent):
    def __init__(self, text: str, settings: "TextComponentSettings | None" = None) -> None:
        self.text = text
        self.settings = settings or TextComponentSettings.default()

        super().__init__()

    def to_dict(self) -> dict:
        return {
            "type": "literal",
            "text": self.text,
            **self.settings.to_dict(),
        }