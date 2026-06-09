from typing import TYPE_CHECKING, Any, Literal, Type


if TYPE_CHECKING:
    from datagen.function.function import Function
    from datagen.utils.minecraft.identifier import Identifier
    from datagen.utils.minecraft.text import Text
    from datagen.utils.repr.itemstack import ItemStack
    from datagen.advancement.criteria import Criteria
    from datagen.advancement.advancement import Advancement

class AdvancementBuilder():
    def __init__(self, advancement: "Advancement"):
        self.advancement = advancement
        self.__criterias = set["Criteria"]()
        self.__requirements = set[str]()
        self.__display = {}
        self.__rewards = {}
    
    def __setitem__(self, key: str, value: Any):
        self.advancement.data[key] = value
    
    def __getitem__(self, key: str) -> Any:
        return self.advancement.data.get(key, None)
    
    def set(self, key: str, value: Any) -> "AdvancementBuilder":
        self.advancement.data[key] = value
        return self
    
    def get[T](self, key: str, as_: T | Type[T] = Any) -> T:
        return self.advancement.data.get(key, None) # type: ignore

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
            "hidden": hidden,
            "background": str(background)
        }
        self.__display = display_data
        return self
    
    def set_criteria(self, criteria: Criteria):
        self.__criterias.add(criteria)
        reqs = set[str]()
        for c in self.__criterias:
            if c.required:
                reqs.add(c.name)
        self.__requirements = reqs
        return self
    
    def set_rewards(
        self, 
        function: Function | None = None,
        experience: int | None = None,
        loot: list[Identifier] | None = None,
        recipe: list[Identifier] | None = None,
    ):
        self.__rewards = {
            "function": function.id if function else None,
            "experience": experience,
            "loot": loot,
            "recipe": recipe
        }
        return self
    
    def seal(self):
        self.advancement.data["display"] = self.__display
        self.advancement.data["criteria"] = {
            c.name: c.data for c in self.__criterias
        }
        self.advancement.data["requirements"] = [list(self.__requirements)]
        self.advancement.data["rewards"] = self.__rewards
        return self.advancement