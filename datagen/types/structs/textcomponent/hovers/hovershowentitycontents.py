
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict

if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.textcomponent import TextComponent

class HoverShowEntityContents(TypedDict):
    type: str
    id: str
    name: NotRequired["TextComponent"]