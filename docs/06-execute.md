# Execute

The `execute` command is one of the most powerful in Minecraft. It lets you run commands conditionally, from a different entity's perspective, at a different position, and much more.

python-datagen wraps it with a fluent builder so you can chain conditions and modifiers in a readable way.

> **What is the `/execute` command?**  
> `/execute` is a super-command that runs other commands with conditions and modifiers. Examples: "execute if the player is holding a diamond", "execute as all zombies within 10 blocks", "execute if the block is stone". It's the foundation of almost all complex logic in datapacks.  
> [Learn more about /execute on the Minecraft Wiki →](https://minecraft.wiki/w/Commands/execute)

---

## Import

```python
from datagen.function.commands.execute import Execute
```

---

## Basic Usage

Build the command by chaining methods, and end with `.RUN(...)`:

```python
~ Execute().AS(TargetSelector.ALL_PLAYERS).RUN(Say("Hello from every player!"))
# → execute as @a run say Hello from every player!
```

---

## Chaining Reference

Every method returns `self` so you can chain them:

```python
Execute()
    .AS(...)
    .AT(...)
    .IF(lambda b: b.entity(...))
    .RUN(...)
```

---

## Modifier Methods

### `AS(target)` — change executor

Runs the command as each matched entity (changes `@s`).

```python
Execute().AS(TargetSelector.ALL_PLAYERS).RUN(Say("I am a player!"))
# → execute as @a run say I am a player!
```

---

### `AT(target)` — change position

Runs from the position of the target entity.

```python
Execute().AT(TargetSelector.SELF).RUN(SetBlock(Position3.HERE, Block("minecraft:stone")))
# → execute at @s run setblock ~ ~ ~ minecraft:stone
```

---

### `ATAS(target)` — AS + AT together

A shorthand for `.AS(target).AT(target)` — changes both executor and position to each target:

```python
Execute().ATAS(TargetSelector.ALL_PLAYERS).RUN(Say("My position!"))
# → execute as @a at @a run say My position!
```

---

### `IN(dimension)` — change dimension

```python
Execute().IN(Identifier.of("minecraft:the_nether")).RUN(my_fn.run())
# → execute in minecraft:the_nether run function my_pack:my_fn
```

---

### `POSITIONED(pos)` — change execution position

```python
Execute().POSITIONED(Position3(0, 64, 0)).RUN(my_fn.run())
# → execute positioned 0 64 0 run function my_pack:my_fn
```

---

### `POSITIONED_AS(target)` — snap position to entity

```python
Execute().POSITIONED_AS(TargetSelector.NEAREST_PLAYER).RUN(my_fn.run())
# → execute positioned as @p run function my_pack:my_fn
```

---

### `ALIGN(axes)` — snap to grid

```python
Execute().ALIGN("xz").RUN(my_fn.run())
# → execute align xz run function my_pack:my_fn
```

---

### `ANCHORED(anchor)` — eye or feet anchor

```python
Execute().ANCHORED("eyes").RUN(my_fn.run())
# → execute anchored eyes run function my_pack:my_fn
```

---

### `FACING(pos)` / `FACING(target, anchor)` — rotation toward target

```python
Execute().FACING(Position3(100, 64, 100)).RUN(my_fn.run())
# → execute facing 100 64 100 run function my_pack:my_fn

Execute().FACING(TargetSelector.NEAREST_PLAYER, "eyes").RUN(my_fn.run())
# → execute facing entity @p eyes run function my_pack:my_fn
```

---

### `ON(relation)` — navigate entity relationships

Switches executor to a related entity (attacker, controller, owner, etc.).

```python
Execute().ON("attacker").RUN(Say("I attacked someone!"))
# → execute on attacker run say I attacked someone!
```

Available relations: `"attacker"`, `"controller"`, `"leasher"`, `"origin"`, `"owner"`, `"passengers"`, `"target"`, `"vehicle"`.

---

### `ROTATED_AS(target)` — copy rotation

```python
Execute().ROTATED_AS(TargetSelector.NEAREST_PLAYER).RUN(my_fn.run())
```

---

## Condition Methods — `IF` and `UNLESS`

Conditions are passed as a lambda that receives a condition builder:

```python
Execute().IF(lambda b: b.entity(TargetSelector.NEAREST_PLAYER)).RUN(Say("There is a nearby player!"))
```

`UNLESS` works identically but negates the condition:

```python
Execute().UNLESS(lambda b: b.entity(TargetSelector.NEAREST_PLAYER)).RUN(Say("No players nearby!"))
```

### Available Conditions

#### `b.entity(selector)` — check if entities exist

```python
Execute().IF(lambda b: b.entity(TargetSelector.NEAREST_PLAYER)).RUN(my_fn.run())
# → execute if entity @p run function ...
```

#### `b.block(block, at)` — check block at position

```python
Execute().IF(lambda b: b.block(Block("minecraft:stone"), BlockPosition.HERE)).RUN(my_fn.run())
# → execute if block ~ ~ ~ minecraft:stone run function ...
```

#### `b.blocks(start, end, dest, condition)` — compare two regions

```python
Execute().IF(lambda b: b.blocks(
    BlockPosition(0,64,0),
    BlockPosition(10,70,10),
    BlockPosition(20,64,0),
    "all"
)).RUN(my_fn.run())
```

#### `b.score(player, comparison, other)` — compare scoreboard values

```python
from datagen.utils.scoreboard.player import ScoreboardPlayer
from datagen.types.util.min import Range

# Compare two players
Execute().IF(lambda b: b.score(
    player_a, ">=", player_b
)).RUN(my_fn.run())

# Compare against a range
Execute().IF(lambda b: b.score(
    my_player, "matches", Range.min(1)
)).RUN(my_fn.run())
# → execute if score @s my_score matches 1.. run function ...
```

#### `b.data(...)` — check NBT data

```python
Execute().IF(lambda b: b.data("entity", TargetSelector.SELF, "Glowing")).RUN(my_fn.run())
# → execute if data entity @s Glowing run function ...
```

#### `b.predicate(predicate)` — check a predicate

```python
Execute().IF(lambda b: b.predicate(my_predicate)).RUN(my_fn.run())
# → execute if predicate my_pack:my_predicate run function ...
```

#### `b.dimension(dimension)` — check current dimension

```python
Execute().IF(lambda b: b.dimension(Identifier.of("minecraft:the_nether"))).RUN(my_fn.run())
```

#### `b.loaded(location)` — check if a chunk is loaded

```python
Execute().IF(lambda b: b.loaded(BlockPosition(0, 64, 0))).RUN(my_fn.run())
```

#### `b.items(...)` — check for items

```python
Execute().IF(lambda b: b.items("entity", TargetSelector.SELF, ItemPath.MAINHAND, Items.DIAMOND)).RUN(my_fn.run())
```

#### `b.biome(biome)` — check current biome

```python
Execute().IF(lambda b: b.biome(Biomes.JUNGLE)).RUN(my_fn.run())
```

---

## Full Example

Run a function on all players that are holding a diamond sword in survival mode, from their position:

```python
from datagen.function.commands.execute import Execute
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings

survival_players = TargetSelector("@a", TargetSelectorSettings(gamemode="survival"))

Execute()
    .AS(survival_players)
    .AT(TargetSelector.SELF)
    .IF(lambda b: b.items("entity", TargetSelector.SELF, ItemPath.MAINHAND, Items.DIAMOND_SWORD))
    .RUN(my_fn.run())
```

---

## Next Steps

- [Text Components →](07-text.md)
- [Script & ScriptBuilder →](10-script-and-scriptbuilder.md)
