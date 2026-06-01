from typing import TYPE_CHECKING, NotRequired, Required

from datagen.types.structs.textcomponent.style import Style
if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.textcomponent import TextComponent


class SelectorObject(Style):
    selector: Required[str]
    separator: NotRequired["TextComponent"]