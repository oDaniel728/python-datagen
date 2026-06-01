from datagen.textcomponents.textcomponent import TextComponent
from datagen.utils.minecraft.identifier import Identifier


class TranslatableTextComponent(TextComponent):
    def __init__(self, identifier: Identifier, fallback: str | None = None) -> None:
        self.identifier = identifier
        self.fallback = fallback

        super().__init__()

    def to_dict(self) -> dict:
        return {
            "type": "translatable",
            "identifier": self.identifier.to_string(),
            **({"fallback": self.fallback} if self.fallback is not None else {}),
        }