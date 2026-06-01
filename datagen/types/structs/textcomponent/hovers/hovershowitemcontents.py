
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict

if TYPE_CHECKING: pass

class HoverShowItemContents(TypedDict):
    id: str
    count: NotRequired[int]
    components: NotRequired[dict]