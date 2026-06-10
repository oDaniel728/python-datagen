# Advancements & Criteria

Advancements are in-game achievements that appear in the Advancements menu. python-datagen lets you define them programmatically using `Advancement`, `AdvancementBuilder`, and `Criteria`.

> **What are Advancements?**  
> Advancements are Minecraft's achievement system — those notifications that pop up in the corner when you do something important. Each advancement has conditions (criteria) the player must meet, and can give rewards like XP, functions, or recipes. With datapacks, you can create your own advancements.  
> [Learn more about Advancements on the Minecraft Wiki →](https://minecraft.wiki/w/Advancement)

---

## Import

```python
from datagen.advancement.advancement import Advancement
from datagen.advancement.advancementbuilder import AdvancementBuilder
from datagen.advancement.criteria import Criteria
```

---

## Advancement

`Advancement(id: Identifier)` creates a new advancement identified by the given `Identifier`.

```python
from datagen.utils.minecraft.identifier import Identifier
from datagen.advancement.advancement import Advancement

my_adv = Advancement(Identifier.of("my_pack:achievements/first_diamond"))
```

### Registering in a namespace

Use `~` (invert) to register the advancement with its namespace — same pattern as `Function` and `Tag`:

```python
~ my_adv
```

### Editing with a builder

There are three equivalent ways to configure an advancement:

**Context manager (recommended)**

```python
with Advancement(Identifier.of("my_pack:achievements/first_diamond")) as builder:
    builder.set_display(
        icon=ItemStack(Items.DIAMOND),
        title=Text.literal("First Diamond"),
        description=Text.literal("Mine your first diamond."),
        frame="task",
        background=Identifier.of("minecraft:textures/gui/advancements/backgrounds/adventure.png"),
    )
    builder.set_criteria(Criteria.inventory_changed(ItemPredicate(item=Items.DIAMOND)))
    builder.set_rewards(experience=10)
# builder.seal() is called automatically on exit
```

**`.do()` callback**

```python
my_adv = Advancement(Identifier.of("my_pack:achievements/first_diamond"))
my_adv.do(lambda b: (
    b.set_display(...),
    b.set_criteria(...),
))
```

**`.open()` manual builder**

```python
builder = my_adv.open()
builder.set_display(...)
builder.seal()
```

---

## AdvancementBuilder

`AdvancementBuilder` is returned when you use a `with Advancement(...) as builder:` block or call `advancement.open()`.

### Methods

| Method | Description |
|--------|-------------|
| `set_display(icon, title, description, frame, background, show_toast, announce_to_chat, hidden)` | Sets the visual appearance |
| `set_criteria(criteria)` | Adds a `Criteria` object. Required criteria are tracked automatically |
| `set_rewards(function, experience, loot, recipe)` | Sets what the player receives upon completing the advancement |
| `seal()` | Finalizes the builder and writes data to the `Advancement`. Called automatically when using `with` |
| `set(key, value)` | Low-level raw key/value setter for the underlying JSON dict |
| `get(key, as_=Any)` | Low-level getter from the underlying JSON dict |

### `set_display` parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | `ItemStack` | required | The icon shown in the advancement tree |
| `title` | `Text.BaseText` | required | Title text shown in the toast and tree |
| `description` | `Text.BaseText` | required | Description shown on hover |
| `frame` | `"task" \| "challenge" \| "goal"` | `"task"` | Frame shape around the icon |
| `background` | `Identifier \| None` | `None` | Background texture for root advancements |
| `show_toast` | `bool` | `True` | Show a toast notification when earned |
| `announce_to_chat` | `bool` | `True` | Announce in chat when earned |
| `hidden` | `bool` | `False` | Hide from the tree until earned |

### `set_rewards` parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `function` | `Function \| None` | Function to run when the advancement is earned |
| `experience` | `int \| None` | XP points to award |
| `loot` | `list[Identifier] \| None` | Loot table IDs to roll |
| `recipe` | `list[Identifier] \| None` | Recipes to unlock |

---

## Criteria

`Criteria` represents a single trigger condition inside an advancement. Each static factory method corresponds to a Minecraft advancement trigger.

```python
from datagen.advancement.criteria import Criteria
```

All static methods return a `Criteria` instance. Pass them to `AdvancementBuilder.set_criteria()`.

### Managing criteria

By default, criteria are required (the player must satisfy all required criteria to complete the advancement). You can mark individual criteria as optional:

```python
c = Criteria.tick()
c.set_required(False)  # not required to complete the advancement
```

You can also change the auto-generated name:

```python
c = Criteria.tick().set_name("my_tick_trigger")
```

---

### Available Triggers

#### `Criteria.impossible()`

Never triggers. Used to create advancements that can only be granted manually via `/advancement grant`.

```python
Criteria.impossible()
```

---

#### `Criteria.tick()`

Fires every game tick. Useful for recurring checks.

```python
Criteria.tick()
```

---

#### `Criteria.inventory_changed(*items, slots=None)`

Fires when the player's inventory changes.

```python
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.minecraft.collections.items import Items

Criteria.inventory_changed(ItemPredicate(item=Items.DIAMOND))
```

`slots` accepts a dict with optional keys `"empty"`, `"full"`, `"occupied"` (each an `int` or `Range`).

---

#### `Criteria.location()`

Fires based on the player's location (no additional conditions — add predicates separately).

```python
Criteria.location()
```

---

#### `Criteria.allay_drop_item_on_block(location, item=None)`

Fires when an Allay drops an item on a block.

```python
from datagen.utils.repr.locationpredicate import LocationPredicate

Criteria.allay_drop_item_on_block(LocationPredicate(...))
```

---

#### `Criteria.any_block_use(*predicates)`

Fires when the player uses any block, with optional location predicates.

---

#### `Criteria.bee_nest_destroyed(block, item, num_bees_inside)`

Fires when a bee nest is destroyed.

```python
from datagen.utils.repr.block import Block
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.types.util.min import Range

Criteria.bee_nest_destroyed(
    Blocks.BEE_NEST,
    ItemPredicate(item=Items.SHEARS),
    num_bees_inside=Range(1, 3)
)
```

---

#### `Criteria.bred_animals(child, parent, partner)`

Fires when the player breeds two animals.

```python
from datagen.utils.repr.entitypredicate import EntityPredicate

Criteria.bred_animals(
    child=EntityPredicate(...),
    parent=EntityPredicate(...),
    partner=EntityPredicate(...)
)
```

---

#### `Criteria.brewed_potion(potion)`

Fires when the player brews a potion.

```python
Criteria.brewed_potion(Identifier.of("minecraft:strength"))
```

---

#### `Criteria.changed_dimension(from_=None, to=None)`

Fires when the player changes dimension.

```python
from datagen.utils.minecraft.collections.dimensions import Dimensions

Criteria.changed_dimension(from_=Dimensions.OVERWORLD, to=Dimensions.THE_NETHER)
```

---

#### `Criteria.construct_beacon(level)`

Fires when the player activates a beacon.

```python
Criteria.construct_beacon(level=4)
Criteria.construct_beacon(level=Range(1, 4))
```

---

#### `Criteria.consume_item(item)`

Fires when the player consumes (eats/drinks) an item.

```python
Criteria.consume_item(ItemPredicate(item=Items.GOLDEN_APPLE))
```

---

#### `Criteria.default_block_use(*predicates)`

Fires when the player uses a block's default action.

---

#### `Criteria.effects_changed(effects, source)`

Fires when the player's status effects change.

```python
from datagen.utils.minecraft.collections.status_effects import StatusEffects

Criteria.effects_changed(
    effects={StatusEffects.SPEED: {"amplifier": 1}},
    source=EntityPredicate(...)
)
```

---

#### `Criteria.enchanted_item(item, levels=None)`

Fires when the player enchants an item.

```python
Criteria.enchanted_item(ItemPredicate(item=Items.DIAMOND_SWORD), levels=Range(1, 30))
```

---

#### `Criteria.enter_block(block)`

Fires when the player enters (steps into) a block.

```python
from datagen.utils.minecraft.collections.blocks import Blocks

Criteria.enter_block(Blocks.WATER)
```

---

#### `Criteria.entity_killed_player(entity, killing_blow)`

Fires when the player is killed by an entity.

```python
from datagen.utils.repr.damagesourcepredicate import DamageSourcePredicate

Criteria.entity_killed_player(
    entity=EntityPredicate(...),
    killing_blow=DamageSourcePredicate(...)
)
```

---

#### `Criteria.filled_bucket(item)`

Fires when the player fills a bucket.

---

#### `Criteria.item_durability_changed(item, delta=None, durability=None)`

Fires when the durability of an item changes.

```python
Criteria.item_durability_changed(
    item=ItemPredicate(item=Items.DIAMOND_PICKAXE),
    durability=Range.min(1)
)
```

---

#### `Criteria.item_used_on_block(*location)`

Fires when the player uses an item on a block.

---

#### `Criteria.placed_block(*location)`

Fires when the player places a block.

---

#### `Criteria.player_hurt_entity(entity, damage)`

Fires when the player damages an entity.

```python
Criteria.player_hurt_entity(
    entity=EntityPredicate(...),
    damage=DamageSourcePredicate(...)
)
```

---

#### `Criteria.player_interacted_with_entity(item, entity)`

Fires when the player interacts with an entity while holding a specific item.

---

#### `Criteria.player_killed_entity(entity, killing_blow)`

Fires when the player kills an entity.

---

#### `Criteria.recipe_crafted(recipe_id, ingredients=None)`

Fires when a recipe is crafted.

```python
Criteria.recipe_crafted(Identifier.of("minecraft:diamond_sword"))
```

---

#### `Criteria.recipe_unlocked(recipe_id)`

Fires when a recipe is unlocked.

---

#### `Criteria.slept_in_bed()`

Fires when the player sleeps in a bed.

---

## Full Example

```python
from datagen.advancement.advancement import Advancement
from datagen.advancement.criteria import Criteria
from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.itemstack import ItemStack

with Namespace("my_pack") as ns:

    with Advancement(Identifier.of("my_pack:achievements/mine_diamond")) as builder:
        builder.set_display(
            icon=ItemStack(Items.DIAMOND),
            title=Text.literal("Diamond Hunter"),
            description=Text.literal("Get a diamond in your inventory."),
            frame="task",
            background=Identifier.of("minecraft:textures/gui/advancements/backgrounds/adventure.png"),
        )
        builder.set_criteria(
            Criteria.inventory_changed(ItemPredicate(item=Items.DIAMOND))
        )
        builder.set_rewards(experience=50)

    ~ Advancement.get(Identifier.of("my_pack:achievements/mine_diamond"))
```

---

## Next Steps

- [Enums & Collections →](14-enums.md)
- [Predicates →](09-predicates.md)
