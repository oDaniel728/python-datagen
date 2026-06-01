from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.hovers.hovershowitem import HoverShowItem
    from datagen.types.structs.textcomponent.hovers.hovershowtext import HoverShowText
    from datagen.types.structs.textcomponent.hovers.hovershowentity import HoverShowEntity

HoverEvent = (
    HoverShowText
    | HoverShowItem
    | HoverShowEntity
)
