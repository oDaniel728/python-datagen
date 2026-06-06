from datagen.recipes.Recipe import Recipe
from datagen.tag.tag import Tag
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack


class RecipeUtils():
    class crafting():
        @staticmethod
        def offer_3x3_compress_decompress(single: Item, compressed: Item) -> tuple[Recipe, Recipe]:
            compress_recipe = Recipe.shaped(
                pattern=[
                    "AAA",
                    "AAA",
                    "AAA"
                ],
                key={
                    "A": single
                },
                result=compressed.get_stack(1)
            )

            decompress_recipe = Recipe.shapeless(
                ingredients=[compressed],
                result=single.get_stack(9)
            )

            return compress_recipe, decompress_recipe

        @staticmethod
        def offer_2x2_compress_decompress(single: Item, compressed: Item) -> tuple[Recipe, Recipe]:
            compress_recipe = Recipe.shaped(
                pattern=[
                    "AA",
                    "AA"
                ],
                key={
                    "A": single
                },
                result=compressed.get_stack(1)
            )

            decompress_recipe = Recipe.shapeless(
                ingredients=[compressed],
                result=single.get_stack(4)
            )

            return compress_recipe, decompress_recipe
        
        @staticmethod
        def offer_surrounded_core(core: Item | Tag[Item], surrounding: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "AAA",
                    "ACA",
                    "AAA"
                ],
                key={
                    "A": surrounding,
                    "C": core
                },
                result=result
            )

        @staticmethod
        def offer_chest_like(surrounding: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "AAA",
                    "A A",
                    "AAA"
                ],
                key={
                    "A": surrounding
                },
                result=result
            )
        
        @staticmethod
        def offer_pillar_like(surrounding: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "A",
                    "A",
                    "A"
                ],
                key={
                    "A": surrounding
                },
                result=result
            )
        
        @staticmethod
        def offer_stick_like(surrounding: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "A",
                    "A"
                ],
                key={
                    "A": surrounding
                },
                result=result
            )
        
        @staticmethod
        def offer_button_like(input: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "A"
                ],
                key={
                    "A": input
                },
                result=result
            )
        
        @staticmethod
        def offer_torch_like(stick: Item | Tag[Item], light_source: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "L",
                    "S"
                ],
                key={
                    "L": light_source,
                    "S": stick
                },
                result=result
            )
        
        @staticmethod
        def offer_wall_like(surrounding: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.shaped(
                pattern=[
                    "AAA",
                    "AAA"
                ],
                key={
                    "A": surrounding
                },
                result=result
            )
    class smelting():
        @staticmethod
        def offer_all_smelts(
            input: Item | Tag[Item], 
            result: ItemStack, 
            experience: float, 
            cooking_time: int, 
            blasting_multi: float, 
            smoking_multi: float
        ) -> tuple[Recipe, Recipe, Recipe]:
            smelting_recipe = Recipe.smelting(
                ingredient=input,
                result=result,
                experience=experience,
                cookingtime=cooking_time
            )

            blasting_recipe = Recipe.blasting(
                ingredient=input,
                result=result,
                experience=experience / blasting_multi,
                cookingtime=int(cooking_time * blasting_multi)
            )

            smoking_recipe = Recipe.smoking(
                ingredient=input,
                result=result,
                experience=experience / smoking_multi,
                cookingtime=int(cooking_time * smoking_multi)
            )

            return smelting_recipe, blasting_recipe, smoking_recipe
        
        @staticmethod
        def offer_smelting_and_blasting(
            input: Item | Tag[Item], 
            result: ItemStack, 
            experience: float, 
            cooking_time: int, 
            blasting_multi: float
        ) -> tuple[Recipe, Recipe]:
            smelting_recipe = Recipe.smelting(
                ingredient=input,
                result=result,
                experience=experience,
                cookingtime=cooking_time
            )

            blasting_recipe = Recipe.blasting(
                ingredient=input,
                result=result,
                experience=experience / blasting_multi,
                cookingtime=int(cooking_time * blasting_multi)
            )

            return smelting_recipe, blasting_recipe
        
        @staticmethod
        def offer_smelting_and_smoking(
            input: Item | Tag[Item], 
            result: ItemStack, 
            experience: float, 
            cooking_time: int, 
            smoking_multi: float
        ) -> tuple[Recipe, Recipe]:
            smelting_recipe = Recipe.smelting(
                ingredient=input,
                result=result,
                experience=experience,
                cookingtime=cooking_time
            )

            smoking_recipe = Recipe.smoking(
                ingredient=input,
                result=result,
                experience=experience / smoking_multi,
                cookingtime=int(cooking_time * smoking_multi)
            )

            return smelting_recipe, smoking_recipe
    class smithing():
        @staticmethod
        def offer_smithing(ingredient: Item | Tag[Item], template: Item | Tag[Item], result: ItemStack) -> Recipe:
            return Recipe.smithing(ingredient, template, result)
        
        @staticmethod
        def offer_upgrade_chain(chain: list[tuple[Item | Tag[Item], Item | Tag[Item], ItemStack]]) -> list[Recipe]:
            recipes = []
            for i, (ingredient, template, result) in enumerate(chain):
                recipe = Recipe.smithing(
                    ingredient=ingredient,
                    template=template,
                    result=result
                )
                recipes.append(recipe)
            return recipes
    class stonecutting():
        @staticmethod
        def offer_stonecutter_multiple(ingredient: Item | Tag[Item], results: list[ItemStack]) -> list[Recipe]:
            recipes = []
            for result in results:
                recipe = Recipe.stonecutting(ingredient, result)
                recipes.append(recipe)
            return recipes