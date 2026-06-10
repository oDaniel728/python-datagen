# Recipes

> **What are Recipes?**  
> Recipes define how players can craft items in Minecraft — in the crafting table, furnace, etc. With datapacks, you can add your own recipes, modify existing ones, or create new crafting types.  
> [Learn more about Recipes on the Minecraft Wiki →](https://minecraft.wiki/w/Recipe)

> **Note:** The recipe system works and produces valid JSON output. However, naming/ID management for recipes is minimal — recipes created with the static helpers get auto-generated temporary IDs. You are expected to set the correct ID before registering them. This area of the library is less polished than the function/command system.

---

## Import

```python
from datagen.recipes.recipe import Recipe
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.minecraft.identifier import Identifier
```

---

## Items and ItemStacks

An `Item` represents an item type. An `ItemStack` is an item with a count (and optional components).

```python
from datagen.utils.minecraft.collections.items import Items

diamond = Items.DIAMOND               # Item object
stack = diamond.get_stack(5)          # ItemStack with count=5
```

---

## Creating Recipes

All recipe types are created through static methods on the `Recipe` class.

### Shaped Crafting

A crafting table recipe with a specific grid layout.

```python
recipe = Recipe.shaped(
    pattern=[
        "AAA",
        " B ",
        " B "
    ],
    key={
        "A": Items.IRON_INGOT,
        "B": Items.STICK
    },
    result=Items.IRON_PICKAXE.get_stack(1)
)
```

The `pattern` is a list of up to 3 strings, each up to 3 characters. Each character maps to a key in the `key` dict. Spaces represent empty slots.

### Shapeless Crafting

A crafting recipe where ingredient positions don't matter.

```python
recipe = Recipe.shapeless(
    ingredients=[Items.BONE, Items.BONE, Items.BONE],
    result=Items.BONE_MEAL.get_stack(3)
)
```

### Smelting (Furnace)

```python
recipe = Recipe.smelting(
    ingredient=Items.RAW_IRON,
    result=Items.IRON_INGOT.get_stack(1),
    experience=0.7,
    cookingtime=200   # ticks (200 = 10 seconds)
)
```

### Blasting (Blast Furnace)

```python
recipe = Recipe.blasting(
    ingredient=Items.RAW_GOLD,
    result=Items.GOLD_INGOT.get_stack(1),
    experience=1.0,
    cookingtime=100   # half the time of smelting
)
```

### Smoking (Smoker)

```python
recipe = Recipe.smoking(
    ingredient=Items.PORKCHOP,
    result=Items.COOKED_PORKCHOP.get_stack(1),
    experience=0.35,
    cookingtime=100
)
```

### Smithing

```python
recipe = Recipe.smithing(
    ingredient=Items.DIAMOND_SWORD,
    template=Items.NETHERITE_UPGRADE_SMITHING_TEMPLATE,
    result=Items.NETHERITE_SWORD.get_stack(1)
)
```

---

## Registering a Recipe

After creating a recipe, assign a proper identifier and register it with your namespace:

```python
recipe = Recipe.shaped(
    pattern=["AA", "AA"],
    key={"A": Items.STONE},
    result=Items.STONE_BRICKS.get_stack(4)
)
recipe.id = Identifier.of("my_pack:stone_bricks_from_stone")

ns.add_recipe(recipe)
```

Or use the `~` operator to register it with whatever namespace is set on it:

```python
~ recipe   # adds it to recipe.namespace
```

---

## Using Tags as Ingredients

Tags can be used instead of specific items in recipes, so any item matching the tag is accepted:

```python
from datagen.tag.itemtag import ItemTag

logs = ItemTag(Identifier.of("minecraft:logs"))

recipe = Recipe.shaped(
    pattern=["AA", "AA"],
    key={"A": logs},
    result=Items.CRAFTING_TABLE.get_stack(1)
)
```

---

## RecipeUtils — Common Patterns

`RecipeUtils` (in `datagenpp/extras/recipes/recipeutils.py`) provides shortcuts for the most common recipe patterns:

```python
from datagenpp.extras.recipes.recipeutils import RecipeUtils

# 3x3 compress / decompress (e.g. 9 iron → 1 iron block, 1 iron block → 9 iron)
compress, decompress = RecipeUtils.crafting.offer_3x3_compress_decompress(
    Items.IRON_INGOT, Items.IRON_BLOCK
)

# 2x2 compress / decompress (e.g. 4 items → 1)
compress, decompress = RecipeUtils.crafting.offer_2x2_compress_decompress(
    Items.QUARTZ, Items.QUARTZ_BLOCK
)

# Item surrounded by 8 of another item
recipe = RecipeUtils.crafting.offer_surrounded_core(
    core=Items.DIAMOND,
    surrounding=Items.IRON_INGOT,
    result=ItemStack(Items.DIAMOND_BLOCK, 1)
)

# Chest-like shape (hollow 3x3)
recipe = RecipeUtils.crafting.offer_chest_like(
    surrounding=Items.OAK_PLANKS,
    result=Items.CHEST.get_stack(1)
)

# Pillar (3 in a column)
recipe = RecipeUtils.crafting.offer_pillar_like(
    surrounding=Items.STICK,
    result=Items.TRIPWIRE_HOOK.get_stack(1)
)

# 2-tall pillar (like a stick)
recipe = RecipeUtils.crafting.offer_stick_like(
    surrounding=Items.OAK_PLANKS,
    result=Items.STICK.get_stack(4)
)

# Single item in center
recipe = RecipeUtils.crafting.offer_button_like(
    input=Items.STONE,
    result=Items.STONE_BUTTON.get_stack(1)
)

# Torch-like pattern
recipe = RecipeUtils.crafting.offer_torch_like(
    stick=Items.STICK,
    light_source=Items.COAL,
    result=Items.TORCH.get_stack(4)
)
```

---

## Raw Recipe Data

If you need a recipe type that isn't covered by the static helpers, you can provide the raw JSON dict directly:

```python
recipe = Recipe(
    Identifier.of("my_pack:special_recipe"),
    {
        "type": "minecraft:crafting_shaped",
        "pattern": ["X"],
        "key": {"X": {"item": "minecraft:stick"}},
        "result": {"id": "minecraft:arrow", "count": 4}
    }
)
ns.add_recipe(recipe)
```

---

## Next Steps

- [Predicates →](09-predicates.md)
- [Script & ScriptBuilder →](10-script-and-scriptbuilder.md)
