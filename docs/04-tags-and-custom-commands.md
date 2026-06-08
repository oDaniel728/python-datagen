# Tags & Custom Commands

---

## Tags

In Minecraft, **tags** are named lists that group items, blocks, or functions together. You can then refer to the entire group by its tag name in commands and recipes.

For example, the vanilla tag `#minecraft:logs` contains all log block types. Instead of listing every log individually, you use the tag.

python-datagen provides three tag classes:

| Class | Groups |
|-------|--------|
| `ItemTag` | Items |
| `BlockTag` | Blocks |
| `FunctionTag` | Functions |

All three work the same way — only the type of values they hold differs.

---

## ItemTag

```python
from datagen.tag.itemtag import ItemTag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.collections.items import Items

# Create a tag
gems = ItemTag(Identifier.of("my_pack:gems"))

# Add items using += or add_value
gems += Items.DIAMOND
gems += Items.EMERALD
gems += Items.AMETHYST_SHARD

# Register it with the namespace
ns.add_tag(gems)
```

This produces `data/my_pack/tags/item/gems.json`:

```json
{
    "values": [
        "minecraft:diamond",
        "minecraft:emerald",
        "minecraft:amethyst_shard"
    ]
}
```

### Including Another Tag Inside a Tag

You can nest tags using the `+=` operator with another tag object:

```python
precious = ItemTag(Identifier.of("my_pack:precious"))
precious += gems            # includes the entire #my_pack:gems tag
precious += Items.GOLD_INGOT
```

---

## BlockTag

```python
from datagen.tag.blocktag import BlockTag
from datagen.utils.minecraft.collections.blocks import Blocks

mineable = BlockTag(Identifier.of("my_pack:soft_blocks"))
mineable += Blocks.DIRT
mineable += Blocks.SAND
mineable += Blocks.GRAVEL

ns.add_tag(mineable)
```

---

## FunctionTag

`FunctionTag` groups functions. The most common use case is registering functions to run on load or every tick via the built-in `minecraft:load` and `minecraft:tick` tags.

```python
with Function(ns / "setup") as setup:
    ~ Say("Pack loaded!")

# Add the function to the load tag
ns.load.add_value(setup)
# This is equivalent to adding setup to minecraft:load
```

You can also create your own function tags and call them from commands:

```python
from datagen.tag.functiontag import FunctionTag
from datagen.function.commands.runfunction import RunFunction

my_tag = FunctionTag(Identifier.of("my_pack:on_death"))
my_tag += setup   # add a function

ns.add_tag(my_tag)

# Call all functions in the tag from a function
with Function(ns / "main") as main_fn:
    ~ RunFunction(my_tag)
```

---

## The `replace` Flag

By default, tags **merge** with vanilla or other pack tags of the same name. If you want your tag to completely replace an existing one, pass `replace=True`:

```python
no_logs = ItemTag(Identifier.of("minecraft:logs"), replace=True)
# This will override the vanilla #minecraft:logs tag entirely
```

Use this carefully — it can break other datapacks or vanilla behaviour.

---

## Checking and Modifying Tags

```python
tag = ItemTag(Identifier.of("my_pack:example"))
tag += Items.DIAMOND

# Check if a value is in the tag
tag.has_value(Items.DIAMOND)   # True

# Remove a value
tag.remove_value(Items.DIAMOND)

# Get all values as a list
tag.to_list()

# Merge another tag's values into this one
other_tag = ItemTag(Identifier.of("my_pack:other"))
tag += other_tag
```

---

## Custom Commands

If you need a command that does not have a dedicated class, use `CustomCommand`:

```python
from datagen.function.commands.customcommand import CustomCommand

with Function(ns / "example") as f:
    ~ CustomCommand("say Hello, world!")
    ~ CustomCommand("time set day")
```

You can pass multiple words separately — they are joined with spaces:

```python
~ CustomCommand("say", "Hello,", "world!")
# → say Hello, world!
```

### Multi-line Custom Commands

You can concatenate commands using `+`:

```python
cmd = CustomCommand("say Line 1")
cmd = cmd + "say Line 2"
~ cmd
```

Or build them incrementally with `+=`:

```python
cmd = CustomCommand("say Line 1")
cmd += "say Line 2"
cmd += CustomCommand("say Line 3")
~ cmd
```

---

## Writing Your Own Command Class

If you find yourself using the same `CustomCommand` pattern many times, create a proper command class instead. Just inherit from `Command` and implement `to_string`:

```python
from datagen.function.commands.command import Command

class MyCommand(Command):
    def __init__(self, message: str, times: int):
        super().__init__()
        self.message = message
        self.times = times

    def to_string(self) -> str:
        # return the raw command string
        return f"say {self.message} x{self.times}"
```

Then use it like any built-in command:

```python
with Function(ns / "example") as f:
    ~ MyCommand("Hello!", 3)
    # → say Hello! x3
```

Your command automatically supports the `~` operator because it inherits from `Command`.

---

## Next Steps

- [Target Selectors →](05-target-selectors.md)
- [Execute →](06-execute.md)
