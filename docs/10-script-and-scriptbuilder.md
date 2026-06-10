# Script & ScriptBuilder

`Script` and `ScriptBuilder` are higher-level tools in the `datagenpp` package. They let you hook into common game events without manually writing the scoreboard/execute boilerplate.

---

## Import

```python
from datagenpp.extras.scripts.script import Script
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder
```

---

## Script

A `Script` is a container that holds:

- **load functions** — run once when the datapack loads (on `/reload`)
- **tick functions** — run every game tick

Instead of manually registering into `minecraft:load` and `minecraft:tick`, you use `Script` to group them, then merge the whole thing into a namespace at once.

### Basic Usage

```python
from datagenpp.extras.scripts.script import Script
from datagen.function.function import Function
from datagen.function.commands.say import Say

with Namespace("my_pack") as ns:
    with Script() as s:

        with Function(ns / "my_setup") as setup_fn:
            ~ Say("Pack loaded!")
        s.on_load(setup_fn)

        with Function(ns / "my_loop") as tick_fn:
            ~ Say("Every tick!")
        s.on_tick(tick_fn)

        s.merge(ns)
```

`s.merge(ns)` automatically:
- Adds each function to the namespace
- Adds load functions to `minecraft:load`
- Adds tick functions to `minecraft:tick`

### Without `with`

```python
s = Script()
s.on_load(my_setup_function)
s.on_tick(my_tick_function)
s.merge(ns)
```

---

## ScriptBuilder

`ScriptBuilder` provides ready-made scripts for common game events. Each method creates all the internal scoreboard/execute machinery and returns a `Script` that you just merge into your namespace.

All builder methods take a `function` parameter — the function that will be called when the event fires. This function can optionally accept a `DataStorage` argument containing context data about the event.

---

### `ScriptBuilder.on_use_of_item(item, function)`

Fires when a player **uses** (right-clicks with) a specific item.

Context data passed to `function`:
- `item` — the item that was used
- `slot` — the slot it was in
- `self` — the player entity

```python
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder
from datagen.utils.minecraft.collections.items import Items

with Function(ns / "on_use_diamond") as handler:
    ~ Say("You used a diamond!")

script = ScriptBuilder.on_use_of_item(Items.DIAMOND, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_killed_by_entity(entity, function)`

Fires when a player is **killed by** a specific entity type.

Context data:
- `killer` — the entity that killed the player
- `self` — the player who died

```python
from datagen.utils.minecraft.collections.entity_types import EntityTypes

with Function(ns / "on_killed_by_zombie") as handler:
    ~ Say("Killed by a zombie!")

script = ScriptBuilder.on_killed_by_entity(EntityTypes.ZOMBIE, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_killed_entity(entity, function)`

Fires when a player **kills** a specific entity type.

Context data:
- `self` — the player who made the kill

```python
with Function(ns / "on_kill_zombie") as handler:
    ~ Say("You killed a zombie!")

script = ScriptBuilder.on_killed_entity(EntityTypes.ZOMBIE, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_item_drop(item, function)`

Fires when a player **drops** a specific item.

Context data:
- `item` — the dropped item identifier
- `slot` — the slot it was in
- `drop` — the dropped item entity
- `self` — the player who dropped it

```python
with Function(ns / "on_drop_diamond") as handler:
    ~ Say("You dropped a diamond!")

script = ScriptBuilder.on_item_drop(Items.DIAMOND, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_item_pickup(item, function)`

Fires when a player **picks up** a specific item.

Context data:
- `self` — the player who picked it up

```python
with Function(ns / "on_pickup_diamond") as handler:
    ~ Say("You picked up a diamond!")

script = ScriptBuilder.on_item_pickup(Items.DIAMOND, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_block_mined(block, function)`

Fires when a player **mines** a specific block.

Context data:
- `self` — the player who mined it
- `item` — the item held (tool used)
- `slot` — the slot that item was in

```python
from datagen.utils.minecraft.collections.blocks import Blocks

with Function(ns / "on_mine_diamond_ore") as handler:
    ~ Say("You mined diamond ore!")

script = ScriptBuilder.on_block_mined(Blocks.DIAMOND_ORE, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_block_placed(block, function)`

Fires when a player **places** a specific block.

Context data:
- `self` — the player who placed the block

```python
with Function(ns / "on_place_tnt") as handler:
    ~ Say("TNT placed!")

script = ScriptBuilder.on_block_placed(Blocks.TNT, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_item_craft(item, function)`

Fires when a player **crafts** a specific item.

Context data:
- `self` — the player who crafted

```python
with Function(ns / "on_craft_bow") as handler:
    ~ Say("You crafted a bow!")

script = ScriptBuilder.on_item_craft(Items.BOW, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_item_broken(item, function)`

Fires when a player **breaks** (destroys by durability) a specific item.

Context data:
- `self` — the player whose item broke

```python
with Function(ns / "on_break_pickaxe") as handler:
    ~ Say("Your pickaxe broke!")

script = ScriptBuilder.on_item_broken(Items.IRON_PICKAXE, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_jump(function)`

Fires every time a player **jumps**.

Context data:
- `self` — the player who jumped

```python
with Function(ns / "on_jump") as handler:
    ~ Say("Jump!")

script = ScriptBuilder.on_jump(handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_walk(cm, function)`

Fires when a player has walked at least `cm` centimetres since the counter was last reset (i.e. since the last trigger). The counter resets after the function fires.

Context data:
- `self` — the player who walked

```python
with Function(ns / "on_walk_100") as handler:
    ~ Say("Walked 100 cm!")

# fires every 100 cm walked
script = ScriptBuilder.on_walk(100, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_crouch(cm, function)`

Fires when a player has crouched at least `cm` centimetres.

Context data:
- `self` — the player

```python
script = ScriptBuilder.on_crouch(50, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_scoreboard_criteria_value_met(criterion, value, function)`

Fires when any player's scoreboard objective (tracked by `criterion`) matches `value`.

Context data:
- `self` — the player
- `value` — the actual score value at trigger time
- `criterion` — the objective name

```python
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.types.util.min import Range

criterion = ObjectiveCriterion.custom("minecraft.jump")
value = Range.min(10)

with Function(ns / "on_ten_jumps") as handler:
    ~ Say("You jumped 10 times!")

script = ScriptBuilder.on_scoreboard_criteria_value_met(criterion, value, handler)
script.merge(ns)
```

---

### `ScriptBuilder.on_each_ticks_for_players(ticks, function)`

Fires for each player every `ticks` game ticks.

Context data:
- `self` — the player

```python
# fire every 20 ticks (1 second) for each player
with Function(ns / "each_second") as handler:
    ~ Say("One second passed!")

script = ScriptBuilder.on_each_ticks_for_players(20, handler)
script.merge(ns)
```

---

## Reading Context Data in the Handler

When a `ScriptBuilder` method calls your function, it passes a `DataStorage` with context data. You can read those values using macro arguments:

```python
from datagen.function.commands._data.datastorage import DataStorage

# The handler function receives macro args from DataStorage
with Function(ns / "on_use_diamond") as handler:
    # Use $(...) macro syntax to read the passed-in data
    ~ Say("$(self) used a diamond!")
```

The exact keys available depend on the event (see each builder method above).

---

## Full Example

```python
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.function.commands.say import Say
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder

def main():
    with DataPack("my_pack", "Event demo") as dp:
        with Namespace("my_pack") as ns:

            # Handler for picking up a diamond
            with Function(ns / "on_diamond_pickup") as pickup_handler:
                ~ Say("You picked up a diamond!")

            ScriptBuilder.on_item_pickup(Items.DIAMOND, pickup_handler).merge(ns)

            # Handler for killing a zombie
            with Function(ns / "on_zombie_kill") as kill_handler:
                ~ Say("Zombie slayer!")

            ScriptBuilder.on_killed_entity(EntityTypes.ZOMBIE, kill_handler).merge(ns)

        dp.add_namespace(ns)
    dp.build()
```

---

## How It Works Internally

Each `ScriptBuilder` method:

1. Creates a **load function** that sets up a scoreboard objective tracking the event
2. Creates a **tick function** that checks the scoreboard every tick using `execute as @a`
3. Creates a **lambda function** that runs your handler with context data and resets the scoreboard counter
4. Wraps everything in a `Script` and returns it

All internal functions are placed in the `temp` namespace with auto-generated names to avoid conflicts with your own functions.

---

## Next Steps

- [DumpGen →](11-dumpgen.md)
- [Advancements →](13-advancements.md)
- [Enums & Collections →](14-enums.md)
- [Configuration →](12-configuration.md)
