# Commands

Every Minecraft command has a corresponding Python class in `datagen/function/commands/`. Each class inherits from `Command` and can be added to a `Function` using the `~` operator.

> **What are Commands?**  
> Commands are instructions you type in Minecraft's chat with `/`. They can do anything: give items, teleport, summon mobs, change the weather, etc. In datapacks, you write commands inside functions and they run automatically.  
> [Full list of commands on the Minecraft Wiki →](https://minecraft.wiki/w/Commands)

---

## How Commands Work

```python
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.datapack.namespace import Namespace

with Namespace("my_pack") as ns:
    with Function(ns / "example") as f:
        ~ Say("Hello!")        # adds: say Hello!
        ~ Say("How are you?")  # adds: say How are you?
```

The `~` operator calls `__invert__` on the command, which appends it to the active function. Outside a `with` block, use `f.add_command(...)` instead.

---

## Available Commands

### `Say`
Broadcasts a message to all players in chat.

```python
from datagen.function.commands.say import Say

~ Say("Hello, world!")
# → say Hello, world!
```

---

### `Tell` / `Msg`
Sends a private message to a specific player.

```python
from datagen.function.commands.tell import Tell

~ Tell(TargetSelector.NEAREST_PLAYER, "Only you can see this")
# → tell @p Only you can see this
```

---

### `Tellraw`
Sends a formatted JSON text message.

```python
from datagen.function.commands.tellraw import Tellraw
from datagen.utils.minecraft.text import Text
from datagen.utils.minecraft.targetselector import TargetSelector

msg = Text.literal("Hello!", bold=True, color="gold")
~ Tellraw(TargetSelector.ALL_PLAYERS, msg)
# → tellraw @a {"type":"text","text":"Hello!","bold":true,"color":"gold"}
```

See [Text Components →](07-text.md) for more on building rich text.

---

### `Title`
Displays a title, subtitle, or action bar message.

```python
from datagen.function.commands.title import Title

~ Title.title(TargetSelector.ALL_PLAYERS, Text.literal("Welcome!"))
~ Title.subtitle(TargetSelector.ALL_PLAYERS, Text.literal("To the server"))
~ Title.actionbar(TargetSelector.ALL_PLAYERS, Text.literal("Info bar"))
~ Title.clear(TargetSelector.ALL_PLAYERS)
~ Title.reset(TargetSelector.ALL_PLAYERS)
~ Title.times(TargetSelector.ALL_PLAYERS, fade_in=10, stay=70, fade_out=20)
```

---

### `Give`
Gives an item to a player.

```python
from datagen.function.commands.give import Give
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack

diamond = Item(Identifier.of("minecraft:diamond"))
~ Give(TargetSelector.NEAREST_PLAYER, ItemStack(diamond, count=5))
# → give @p minecraft:diamond 5
```

---

### `Kill`
Kills one or more entities.

```python
from datagen.function.commands.kill import Kill

~ Kill(TargetSelector.SELF)
# → kill @s

~ Kill(TargetSelector.ALL_ENTITIES)
# → kill @e
```

---

### `Teleport`
Teleports entities to a target or position.

```python
from datagen.function.commands.teleport import Teleport
from datagen.utils.repr.position3 import Position3

# Teleport self to coordinates
~ Teleport(TargetSelector.SELF, Position3(100, 64, 200))

# Teleport self to another entity
~ Teleport(TargetSelector.SELF, TargetSelector.NEAREST_PLAYER)

# Teleport to coordinates (shorthand — self implied)
~ Teleport(Position3(0, 64, 0))
```

---

### `Summon`
Spawns an entity.

```python
from datagen.function.commands.summon import Summon
from datagen.utils.minecraft.collections.entity_types import EntityTypes

~ Summon(EntityTypes.ZOMBIE, Position3(0, 64, 0))
```

---

### `Effect`
Applies or clears a status effect.

```python
from datagen.function.commands.effect import Effect
from datagen.utils.minecraft.collections.mob_effects import MobEffects

~ Effect.give(TargetSelector.SELF, MobEffects.SPEED, duration=200, amplifier=1)
~ Effect.clear(TargetSelector.SELF, MobEffects.SPEED)
~ Effect.clear_all(TargetSelector.SELF)
```

---

### `Enchant`
Enchants the item a player is holding.

```python
from datagen.function.commands.enchant import Enchant
from datagen.utils.minecraft.collections.enchantments import Enchantments

~ Enchant(TargetSelector.SELF, Enchantments.SHARPNESS, level=5)
```

---

### `Experience` / `XP`
Gives, sets, or queries experience.

```python
from datagen.function.commands.experience import Experience

~ Experience.add(TargetSelector.SELF, 100, "points")
~ Experience.set(TargetSelector.SELF, 5, "levels")
```

---

### `Gamemode`
Changes a player's game mode.

```python
from datagen.function.commands.gamemode import Gamemode

~ Gamemode("creative", TargetSelector.SELF)
~ Gamemode("survival", TargetSelector.ALL_PLAYERS)
```

---

### `Gamerule`
Gets or sets a game rule.

```python
from datagen.function.commands.gamerule import Gamerule

~ Gamerule("keepInventory", True)
~ Gamerule("doDaylightCycle", False)
```

---

### `Difficulty`
Sets the world difficulty.

```python
from datagen.function.commands.difficulty import Difficulty

~ Difficulty("hard")
```

---

### `Scoreboard`
Manages scoreboards. See the [scoreboard section below](#scoreboard).

---

### `SetBlock`
Places a block at a position.

```python
from datagen.function.commands.setblock import SetBlock
from datagen.utils.repr.block import Block

~ SetBlock(Position3(0, 64, 0), Block("minecraft:stone"))
~ SetBlock(Position3(~0, ~1, ~0), Block("minecraft:air"), mode="destroy")
```

---

### `Fill`
Fills a region with blocks.

```python
from datagen.function.commands.fill import Fill
from datagen.utils.repr.block import Block

~ Fill(Position3(0, 64, 0), Position3(10, 70, 10), Block("minecraft:glass"))
```

---

### `Clone`
Copies blocks from one region to another.

```python
from datagen.function.commands.clone import Clone

~ Clone(Position3(0,64,0), Position3(10,70,10), Position3(20,64,0))
```

---

### `Particle`
Spawns a particle effect.

```python
from datagen.function.commands.particle import Particle
from datagen.utils.minecraft.collections.particle_types import ParticleTypes

~ Particle(ParticleTypes.FLAME, Position3(0, 64, 0))
```

---

### `Sound`
Plays a sound.

```python
from datagen.function.commands.sound import Sound
from datagen.utils.minecraft.collections.sounds import Sounds

~ Sound(Sounds.ENTITY_PLAYER_LEVELUP, "master", TargetSelector.ALL_PLAYERS, Position3(0,64,0))
```

---

### `StopSound`
Stops a playing sound.

```python
from datagen.function.commands.stopsound import StopSound

~ StopSound(TargetSelector.ALL_PLAYERS)
```

---

### `Tag`
Manages entity tags (not to be confused with data tags).

```python
from datagen.function.commands.tag import Tag as TagCmd

~ TagCmd.add(TargetSelector.SELF, "my_tag")
~ TagCmd.remove(TargetSelector.SELF, "my_tag")
```

---

### `Team`
Manages teams.

```python
from datagen.function.commands.team import Team

~ Team.add("red_team", Text.literal("Red Team", color="red"))
~ Team.join("red_team", TargetSelector.SELF)
~ Team.leave(TargetSelector.SELF)
~ Team.remove("red_team")
```

---

### `Schedule`
Schedules a function to run after a delay.

```python
from datagen.function.commands.schedule import Schedule

~ Schedule.function(my_fn, delay=20)          # 20 ticks = 1 second
~ Schedule.function(my_fn, delay=100, mode="replace")
~ Schedule.clear(my_fn)
```

---

### `Reload`
Reloads the datapack.

```python
from datagen.function.commands.reload import Reload

~ Reload()
```

---

### `Return`
Returns a value from a function (stops execution).

```python
from datagen.function.commands._return import Return

~ Return(1)           # return 1
~ Return.run(my_fn.run())  # return the result of another function
~ Return.fail()       # return failure
```

---

### `Data`
Reads and writes NBT data on entities, blocks, or storage.

```python
from datagen.function.commands.data import Data

~ Data.get_entity(TargetSelector.SELF, "Health")
~ Data.set_entity(TargetSelector.SELF, "Invulnerable", "1b")
```

---

### `Loot`
Drops loot table items.

```python
from datagen.function.commands.loot import Loot

~ Loot.spawn(Position3(0,64,0), Identifier.of("minecraft:entities/zombie"))
```

---

### `Locate`
Locates a structure or biome.

```python
from datagen.function.commands.locate import Locate

~ Locate.structure(Identifier.of("minecraft:village/plains"))
~ Locate.biome(Identifier.of("minecraft:jungle"))
```

---

### `Damage`
Deals damage to an entity.

```python
from datagen.function.commands.damage import Damage

~ Damage(TargetSelector.SELF, amount=5, damage_type=Identifier.of("minecraft:generic"))
```

---

### `Tick`
Controls the game tick rate.

```python
from datagen.function.commands.tick import Tick

~ Tick.freeze()
~ Tick.unfreeze()
~ Tick.set(20)        # normal speed
~ Tick.sprint(100)    # run 100 ticks as fast as possible
```

---

### `Random`
Generates a random value or rolls dice.

```python
from datagen.function.commands.random import Random

~ Random.value(1, 6)   # random number between 1 and 6
~ Random.roll("1d6")
```

---

### `Scoreboard`

Scoreboard management is done through the `Scoreboard` helper class.

```python
from datagen.function.commands.scoreboard import Scoreboard
from datagen.utils.minecraft.text import Text
from datagen.utils.scoreboard.criterion import ObjectiveCriterion

# Create an objective
obj = Scoreboard.objective("my_score", Text.literal("My Score"), ObjectiveCriterion.DUMMY)

# Get a player reference
player = obj.player(TargetSelector.SELF)

# Add commands
~ obj.add()           # /scoreboard objectives add my_score dummy "My Score"
~ player.set(10)      # /scoreboard players set @s my_score 10
~ player.add(5)       # /scoreboard players add @s my_score 5
~ player.remove(2)    # /scoreboard players remove @s my_score 2
~ player.reset()      # /scoreboard players reset @s my_score
~ player.get()        # /scoreboard players get @s my_score
```

---

## Other Available Commands

The following commands are available but not shown in detail here. Their usage follows the same pattern as the above.

| Class | Minecraft command |
|-------|------------------|
| `BossBar` | `/bossbar` |
| `Clear` | `/clear` |
| `Debug` | `/debug` |
| `DefaultGamemode` | `/defaultgamemode` |
| `FillBiome` | `/fillbiome` |
| `ForceLoad` | `/forceload` |
| `Help` | `/help` |
| `Item` | `/item` |
| `Kick` | `/kick` |
| `List` | `/list` |
| `Publish` | `/publish` |
| `Ride` | `/ride` |
| `Seed` | `/seed` |
| `SetWorldSpawn` | `/setworldspawn` |
| `SpawnPoint` | `/spawnpoint` |
| `Spectate` | `/spectate` |
| `SpreadPlayers` | `/spreadplayers` |
| `Teammsg` | `/teammsg` |
| `Time` | `/time` |
| `Trigger` | `/trigger` |
| `Weather` | `/weather` |

---

## Next Steps

- [Tags & Custom Commands →](04-tags-and-custom-commands.md)
- [Target Selectors →](05-target-selectors.md)
- [Execute →](06-execute.md)
