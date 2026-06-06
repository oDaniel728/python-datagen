import json
from pathlib import Path

from datagen.globals import RECIPES_PATH
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.simplefile import SimpleFile


class Recipe():

    __recipes: dict[Identifier, "Recipe"] = {}

    def __new__(cls, id: Identifier, data: dict):
        if id in cls.__recipes:
            instance = cls.__recipes[id]
            instance._data = data
            return instance
        instance = super().__new__(cls)
        cls.__recipes[id] = instance
        return instance

    def __init__(self, id: Identifier, data: dict) -> None:
        from datagen.datapack.namespace import Namespace

        self._data = data
        self.id = id
        self.namespace = Namespace.get(id)
        Recipe.__recipes[id] = self
        self.namespace.add_recipe(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Recipe) and self.id == other.id

    def to_dict(self) -> dict:
        return self._data

    def to_string(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def get_filepath(self) -> Path:
        return Path(RECIPES_PATH) / (self.id.get_path().replace(".", "/").lower() + ".json")

    def to_file(self) -> SimpleFile:
        return SimpleFile(self.get_filepath(), self.to_string())

    @staticmethod
    def shaped(pattern: list[str], key: dict[str, Item | Tag[Item]], result: ItemStack) -> "Recipe":
        return Recipe(Identifier.of("temp", f"shaped_{len(Recipe.__recipes)}"), {
            "type": "minecraft:crafting_shaped",
            "pattern": pattern,
            "key": {k: v.id.to_string() for k, v in key.items()},
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            }
        })

    @staticmethod
    def shapeless(ingredients: list[Item | Tag[Item]], result: ItemStack) -> "Recipe":
        return Recipe(Identifier.of("temp", f"shapeless_{len(Recipe.__recipes)}"), {
            "type": "minecraft:crafting_shapeless",
            "ingredients": [ingredient.id.to_string() for ingredient in ingredients],
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            }
        })

    @staticmethod
    def smelting(ingredient: Item | Tag[Item], result: ItemStack, experience: float = 0.0, cookingtime: int = 200) -> "Recipe":
        return Recipe(Identifier.of("temp", f"smelting_{len(Recipe.__recipes)}"), {
            "type": "minecraft:smelting",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            },
            "experience": experience,
            "cookingtime": cookingtime
        })

    @staticmethod
    def blasting(ingredient: Item | Tag[Item], result: ItemStack, experience: float = 0.0, cookingtime: int = 100) -> "Recipe":
        return Recipe(Identifier.of("temp", f"blasting_{len(Recipe.__recipes)}"), {
            "type": "minecraft:blasting",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            },
            "experience": experience,
            "cookingtime": cookingtime
        })
    
    @staticmethod
    def smoking(ingredient: Item | Tag[Item], result: ItemStack, experience: float = 0.0, cookingtime: int = 100) -> "Recipe":
        return Recipe(Identifier.of("temp", f"smoking_{len(Recipe.__recipes)}"), {
            "type": "minecraft:smoking",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            },
            "experience": experience,
            "cookingtime": cookingtime
        })

    @staticmethod
    def smithing(ingredient: Item | Tag[Item], template: Item | Tag[Item], result: ItemStack) -> "Recipe":
        return Recipe(Identifier.of("temp", f"smithing_{len(Recipe.__recipes)}"), {
            "type": "minecraft:smithing",
            "ingredient": ingredient.id.to_string(),
            "template": template.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            }
        })

    @staticmethod
    def stonecutting(ingredient: Item | Tag[Item], result: ItemStack) -> "Recipe":
        return Recipe(Identifier.of("temp", f"stonecutting_{len(Recipe.__recipes)}"), {
            "type": "minecraft:stonecutting",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            }
        })

    @staticmethod
    def transmute(ingredient: Item | Tag[Item], result: ItemStack) -> "Recipe":
        return Recipe(Identifier.of("temp", f"transmute_{len(Recipe.__recipes)}"), {
            "type": "minecraft:transmuting",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            }
        })
    
    @staticmethod
    def campfire_cooking(ingredient: Item | Tag[Item], result: ItemStack, experience: float = 0.0, cookingtime: int = 100) -> "Recipe":
        return Recipe(Identifier.of("temp", f"campfire_cooking_{len(Recipe.__recipes)}"), {
            "type": "minecraft:campfire_cooking",
            "ingredient": ingredient.id.to_string(),
            "result": {
                "count": result.count,
                "item": result.item.id.to_string(),
                "components": result.item.nbt
            },
            "experience": experience,
            "cookingtime": cookingtime
        })