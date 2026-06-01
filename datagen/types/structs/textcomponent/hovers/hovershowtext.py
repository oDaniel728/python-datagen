
from typing import TYPE_CHECKING, Literal, TypedDict


if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.textcomponent import TextComponent

class HoverShowText(TypedDict):
    action: Literal["show_text"]
    contents: "TextComponent"