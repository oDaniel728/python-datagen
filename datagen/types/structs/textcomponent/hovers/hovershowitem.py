
from typing import TYPE_CHECKING, Literal, TypedDict


if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.hovers.hovershowitemcontents import HoverShowItemContents

class HoverShowItem(TypedDict):
    action: Literal["show_item"]
    contents: HoverShowItemContents