
from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.component import Component
    from datagen.types.structs.textcomponent.events.clickevent import ClickEvent
    from datagen.types.structs.textcomponent.events.hoverevent import HoverEvent


class Style(TypedDict, total=False):

    color: str

    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool

    insertion: str
    font: str

    clickEvent: "ClickEvent"
    hoverEvent: "HoverEvent"

    extra: list["Component"]
