# Enums & Collections

python-datagen provides pre-built collections for every major Minecraft registry. These are static classes whose members are typed wrappers, ready to be passed directly to any API that accepts that type.

All collections live under `datagen.utils.minecraft.collections`.

> **What are these Collections?**  
> These are ready-made lists of everything in Minecraft: items, blocks, entities, biomes, effects, enchantments... Instead of memorising names or typing `Identifier.of("...")` every time, you use `Items.DIAMOND`, `EntityTypes.ZOMBIE`, `Biomes.FOREST`. Your editor shows suggestions as you type.  
> [See the full item list on the Minecraft Wiki →](https://minecraft.wiki/w/Item)  
> [See the status effects list on the Minecraft Wiki →](https://minecraft.wiki/w/Effect)

---

## Overview

| Collection class | Module | Value type | Use with |
|-----------------|--------|-----------|----------|
| `Items` | `...collections.items` | `Item` | commands, predicates, criteria, settings |
| `Blocks` | `...collections.blocks` | `Block` | commands, predicates, criteria |
| `EntityTypes` | `...collections.entity_types` | `EntityType` | selectors, ScriptBuilder, criteria |
| `Dimensions` | `...collections.dimensions` | `Dimension` | criteria, predicates |
| `Biomes` | `...collections.biomes` | `Biome` | predicates |
| `Sounds` | `...collections.sounds` | `Sound` | `PlaySound` command |
| `SoundSources` | `...collections.soundchannels` | `SoundSource` | `PlaySound` command |
| `EquipmentSlots` | `...collections.equipment_slots` | `EquipmentSlot` | item settings, predicates |
| `Gamemodes` | `...collections.gamemodes` | `MCGamemode` | selectors, criteria |
| `Enchantments` | `...collections.enchantments` | `Enchantment` | item settings, predicates |
| `MobEffects` | `...collections.mob_effects` | `MobEffect` | effect commands, predicates |
| `Attributes` | `...collections.attributes` | `Attribute` | attribute commands |
| `Instruments` | `...collections.instruments` | `Instrument` | item settings |
| `Particles` | `...collections.particle_types` | `Particle` | particle commands |
| `Structures` | `...collections.structures` | `Structure` | structure-related work |
| `VillagerProfessions` | `...collections.villager_professions` | `VillagerProfession` | entity predicates |
| `VillagerTypes` | `...collections.villager_types` | `VillagerType` | entity predicates |
| `BlockTypes` | `...collections.block_types` | `BlockType` | predicates |
| `DamageTypes` | `...collections.damage_types` | `DamageType` | damage predicates |

---

## Items

```python
from datagen.utils.minecraft.collections.items import Items
```

Contains every vanilla item as an `Item` instance. Used wherever an `Item` is accepted.

```python
Items.DIAMOND
Items.GOLDEN_APPLE
Items.DIAMOND_SWORD
Items.NETHERITE_PICKAXE
# ... hundreds of members
```

**Example:**

```python
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.repr.itempredicate import ItemPredicate

predicate = ItemPredicate(item=Items.DIAMOND)
```

---

## Blocks

```python
from datagen.utils.minecraft.collections.blocks import Blocks
```

Contains every vanilla block as a `Block` instance.

```python
Blocks.DIAMOND_ORE
Blocks.GRASS_BLOCK
Blocks.WATER
Blocks.BEE_NEST
# ...
```

**Example (criteria):**

```python
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.advancement.criteria import Criteria

Criteria.enter_block(Blocks.WATER)
Criteria.placed_block()  # add a Predicate for the block
```

---

## EntityTypes

```python
from datagen.utils.minecraft.collections.entity_types import EntityTypes
```

Contains every vanilla entity type as an `EntityType` instance.

```python
EntityTypes.ZOMBIE
EntityTypes.CREEPER
EntityTypes.PLAYER
EntityTypes.ITEM
EntityTypes.ARROW
# ...
```

**Example (ScriptBuilder):**

```python
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder

ScriptBuilder.on_killed_entity(EntityTypes.ZOMBIE, handler)
```

**Example (TargetSelector):**

```python
from datagen.utils.minecraft.targetselector import TargetSelector

TargetSelector.nearest(EntityTypes.ITEM)
```

---

## Dimensions

```python
from datagen.utils.minecraft.collections.dimensions import Dimensions
```

| Member | Value |
|--------|-------|
| `Dimensions.OVERWORLD` | `minecraft:overworld` |
| `Dimensions.OVERWORLD_CAVES` | `minecraft:overworld_caves` |
| `Dimensions.THE_NETHER` | `minecraft:the_nether` |
| `Dimensions.THE_END` | `minecraft:the_end` |

**Example:**

```python
from datagen.advancement.criteria import Criteria
from datagen.utils.minecraft.collections.dimensions import Dimensions

Criteria.changed_dimension(from_=Dimensions.OVERWORLD, to=Dimensions.THE_NETHER)
```

---

## Biomes

```python
from datagen.utils.minecraft.collections.biomes import Biomes
```

Contains every vanilla biome as a `Biome` instance.

```python
Biomes.FOREST
Biomes.DESERT
Biomes.DEEP_DARK
Biomes.CHERRY_GROVE
Biomes.THE_END
# ...
```

---

## Sounds

```python
from datagen.utils.minecraft.collections.sounds import Sounds
```

Contains every vanilla sound event as a `Sound` instance. Used with `PlaySound`.

```python
Sounds.ENTITY_PLAYER_LEVELUP
Sounds.BLOCK_NOTE_BLOCK_PLING
Sounds.ENTITY_LIGHTNING_BOLT_THUNDER
# ...
```

---

## SoundSources

```python
from datagen.utils.minecraft.collections.soundchannels import SoundSources
```

| Member | Value |
|--------|-------|
| `SoundSources.MASTER` | `master` |
| `SoundSources.MUSIC` | `music` |
| `SoundSources.RECORD` | `record` |
| `SoundSources.WEATHER` | `weather` |
| `SoundSources.BLOCK` | `block` |
| `SoundSources.HOSTILE` | `hostile` |
| `SoundSources.NEUTRAL` | `neutral` |
| `SoundSources.PLAYER` | `player` |
| `SoundSources.AMBIENT` | `ambient` |

**Example:**

```python
from datagen.function.commands.playsound import PlaySound
from datagen.utils.minecraft.collections.sounds import Sounds
from datagen.utils.minecraft.collections.soundchannels import SoundSources

~ PlaySound(Sounds.ENTITY_PLAYER_LEVELUP, SoundSources.PLAYER, TargetSelector.SELF)
```

---

## EquipmentSlots

```python
from datagen.utils.minecraft.collections.equipment_slots import EquipmentSlots
```

| Member | Value |
|--------|-------|
| `EquipmentSlots.MAINHAND` | `mainhand` |
| `EquipmentSlots.OFFHAND` | `offhand` |
| `EquipmentSlots.HEAD` | `head` |
| `EquipmentSlots.CHEST` | `chest` |
| `EquipmentSlots.LEGS` | `legs` |
| `EquipmentSlots.FEET` | `feet` |
| `EquipmentSlots.BODY` | `body` |

---

## Gamemodes

```python
from datagen.utils.minecraft.collections.gamemodes import Gamemodes
```

| Member | Value |
|--------|-------|
| `Gamemodes.SURVIVAL` | `survival` |
| `Gamemodes.CREATIVE` | `creative` |
| `Gamemodes.ADVENTURE` | `adventure` |
| `Gamemodes.SPECTATOR` | `spectator` |

**Example:**

```python
from datagen.function.commands.gamemode import Gamemode
from datagen.utils.minecraft.collections.gamemodes import Gamemodes

~ Gamemode(Gamemodes.CREATIVE, TargetSelector.SELF)
```

---

## Enchantments

```python
from datagen.utils.minecraft.collections.enchantments import Enchantments
```

Contains every vanilla enchantment.

```python
Enchantments.SHARPNESS
Enchantments.UNBREAKING
Enchantments.SILK_TOUCH
Enchantments.FORTUNE
# ...
```

---

## MobEffects / StatusEffects

```python
from datagen.utils.minecraft.collections.mob_effects import MobEffects
# or
from datagen.utils.minecraft.collections.status_effects import StatusEffects
```

Contains every vanilla potion/status effect.

```python
MobEffects.SPEED
MobEffects.STRENGTH
MobEffects.REGENERATION
# ...
```

**Example:**

```python
from datagen.function.commands.effect import Effect
from datagen.utils.minecraft.collections.mob_effects import MobEffects

~ Effect.give(TargetSelector.SELF, MobEffects.SPEED, duration=60, amplifier=1)
```

---

## Attributes

```python
from datagen.utils.minecraft.collections.attributes import Attributes
```

Contains every vanilla entity attribute.

```python
Attributes.MAX_HEALTH
Attributes.ATTACK_DAMAGE
Attributes.MOVEMENT_SPEED
# ...
```

---

## Particles

```python
from datagen.utils.minecraft.collections.particle_types import Particles
```

Contains every vanilla particle type.

```python
Particles.FLAME
Particles.HEART
Particles.EXPLOSION
# ...
```

---

## VillagerProfessions

```python
from datagen.utils.minecraft.collections.villager_professions import VillagerProfessions
```

```python
VillagerProfessions.FARMER
VillagerProfessions.LIBRARIAN
VillagerProfessions.BLACKSMITH
# ...
```

---

## VillagerTypes

```python
from datagen.utils.minecraft.collections.villager_types import VillagerTypes
```

```python
VillagerTypes.PLAINS
VillagerTypes.DESERT
VillagerTypes.TAIGA
# ...
```

---

## Instruments

```python
from datagen.utils.minecraft.collections.instruments import Instruments
```

Used with goat horn items.

```python
Instruments.PONDER_GOAT_HORN
Instruments.SING_GOAT_HORN
# ...
```

---

## Structures

```python
from datagen.utils.minecraft.collections.structures import Structures
```

```python
Structures.VILLAGE_PLAINS
Structures.STRONGHOLD
Structures.OCEAN_MONUMENT
# ...
```

---

## How dumpgen keeps these up to date

These collection files are auto-generated by `dumpgen/` from Minecraft's data exports. Run `python dumpgen/gen.py` to regenerate them after a game update. See [DumpGen →](11-dumpgen.md).

---

## Next Steps

- [Advancements →](13-advancements.md)
- [Script & ScriptBuilder →](10-script-and-scriptbuilder.md)
