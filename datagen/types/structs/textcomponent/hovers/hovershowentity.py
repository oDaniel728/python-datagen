from typing import TYPE_CHECKING, TypedDict, Literal

if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.hovers.hovershowentitycontents import HoverShowEntityContents


class HoverShowEntity(TypedDict):
    action: Literal["show_entity"]
    contents: HoverShowEntityContents