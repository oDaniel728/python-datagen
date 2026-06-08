# Target Selectors

A **target selector** tells Minecraft which entities a command should affect. In python-datagen, target selectors are represented by the `TargetSelector` class.

---

## Import

```python
from datagen.utils.minecraft.targetselector import TargetSelector
```

---

## Built-in Selectors

These are available as class attributes on `TargetSelector`:

| Attribute | Minecraft selector | Description |
|-----------|-------------------|-------------|
| `TargetSelector.SELF` | `@s` | The entity running the command |
| `TargetSelector.NEAREST_PLAYER` | `@p` | The nearest player |
| `TargetSelector.ALL_PLAYERS` | `@a` | All players |
| `TargetSelector.ALL_ENTITIES` | `@e` | All entities |
| `TargetSelector.RANDOM_PLAYER` | `@r` | A random player |
| `TargetSelector.NEAREST_ENTITY` | `@e[sort=nearest,limit=1]` | The nearest entity |
| `TargetSelector.RANDOM_ENTITY` | `@e[sort=random,limit=1]` | A random entity |

```python
~ Kill(TargetSelector.ALL_ENTITIES)
# → kill @e

~ Give(TargetSelector.NEAREST_PLAYER, ItemStack(Items.DIAMOND, 1))
# → give @p minecraft:diamond 1
```

---

## Selectors with Filters

Use `TargetSelectorSettings` to add filters to a selector:

```python
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.collections.entity_types import EntityTypes

# All zombies within 10 blocks
nearby_zombies = TargetSelector(
    "@e",
    TargetSelectorSettings(
        type=EntityTypes.ZOMBIE,
        distance=Range(0, 10)
    )
)

~ Kill(nearby_zombies)
# → kill @e[type=minecraft:zombie,distance=..10]
```

### Available Filter Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `x`, `y`, `z` | `int \| Range` | Center position of selection |
| `dx`, `dy`, `dz` | `int \| Range` | Volume size in each axis |
| `distance` | `int \| Range` | Distance from the command source |
| `x_rotation`, `y_rotation` | `int \| Range` | Pitch / yaw filter |
| `scores` | `dict[str, int \| Range]` | Scoreboard filter |
| `tag` | `str` | Entity must have this tag |
| `team` | `str` | Entity must be on this team |
| `name` | `str` | Entity display name |
| `type` | `EntityType \| str` | Entity type filter |
| `predicate` | `Identifier` | Must match this predicate |
| `nbt` | `dict` | NBT filter |
| `sort` | `"nearest" \| "furthest" \| "random" \| "arbitrary"` | Sort order |
| `limit` | `int` | Maximum number of targets |
| `level` | `int \| Range` | Player XP level range |
| `gamemode` | `"survival" \| "creative" \| "adventure" \| "spectator"` | Gamemode filter |

---

## Convenience Static Methods

`TargetSelector` also offers static helpers that build common patterns:

```python
from datagen.utils.minecraft.collections.entity_types import EntityTypes

# The nearest zombie
TargetSelector.nearest(EntityTypes.ZOMBIE)
# → @e[type=minecraft:zombie,sort=nearest,limit=1]

# The furthest skeleton
TargetSelector.furthest(EntityTypes.SKELETON)

# A random creeper
TargetSelector.random(EntityTypes.CREEPER)

# An arbitrary blaze (no particular order)
TargetSelector.arbitrary(EntityTypes.BLAZE, limit=5)
```

---

## Ranges

`Range` is used in filters that accept a min/max value:

```python
from datagen.types.util.min import Range

Range(0, 10)     # 0..10  — between 0 and 10
Range.min(5)     # 5..    — 5 or more
Range.max(10)    # ..10   — 10 or less
```

Example:

```python
# All players within 5 to 20 blocks
TargetSelector("@a", TargetSelectorSettings(distance=Range(5, 20)))
```

---

## Converting to String

`TargetSelector` converts to the raw Minecraft selector string when used in a command. You can also convert it explicitly:

```python
sel = TargetSelector.ALL_PLAYERS
str(sel)      # "@a"
~sel          # "@a"  (using __invert__)
sel.to_string()  # "@a"
```

---

## Next Steps

- [Execute →](06-execute.md) — complex conditional logic using `execute`
