from typing import TYPE_CHECKING, Any, Literal, Type

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.itemstack import ItemStack

if TYPE_CHECKING:
    from datagen.advancement.advancement import Advancement

class AdvancementBuilder():
    def __init__(self, advancement: "Advancement"):
        self.advancement = advancement
    
    def __setitem__(self, key: str, value: Any):
        self.advancement.data[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self.advancement.data[key]
    
    def set(self, key: str, value: Any) -> "AdvancementBuilder":
        self.advancement.data[key] = value
        return self
    
    def get[T](self, key: str, as_: T | Type[T] = Any) -> T:
        return self.advancement.data[key]

    _TFrame = Literal["task", "challenge", "goal"]
    def set_display(
        self, 
        icon: ItemStack, 
        title: Text.BaseText, 
        description: Text.BaseText, 
        frame: _TFrame = "task", 
        background: Identifier | None = None, 
        show_toast: bool = True, 
        announce_to_chat: bool = True, 
        hidden: bool = False
    ) -> "AdvancementBuilder":
        display_data = {
            "icon": {
                "id": ~icon.item.id,
                "count": icon.count,
                "components": icon.item.settings.get_components()
            },
            "title": title.to_dict(),
            "description": description.to_dict(),
            "frame": frame,
            "show_toast": show_toast,
            "announce_to_chat": announce_to_chat,
            "hidden": hidden
        }
        if background is not None:
            display_data["background"] = background
        self.advancement.data["display"] = display_data
        return self