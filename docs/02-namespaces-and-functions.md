# Namespaces & Functions

This page explains how to organize your datapack using Namespaces and Functions.

> **What are Namespaces and Functions?**  
> In Minecraft, everything you create in a datapack needs a **namespace** (a prefix before the colon, like `mypack:name`). A **function** is a list of commands that the game runs in sequence — like a script. You create `.mcfunction` files and the game reads them.  
> [Learn more about Functions on the Minecraft Wiki →](https://minecraft.wiki/w/Function_(Java_Edition))  
> [Learn more about Namespaced IDs on the Minecraft Wiki →](https://minecraft.wiki/w/Namespaced_ID)

---

## Namespaces

A **Namespace** maps to a folder inside `data/` in your datapack. Every function, tag, predicate, and recipe lives under a namespace.

In Minecraft, a namespace is the part before the `:` in an identifier. For example, in `minecraft:load`, the namespace is `minecraft`.

### Creating a Namespace

```python
from datagen.datapack.namespace import Namespace

ns = Namespace("my_pack")
```

### Built-in Namespaces

Two namespaces are always available as class attributes:

| Attribute | Namespace name | Purpose |
|-----------|---------------|---------|
| `Namespace.minecraft` | `minecraft` | Used to register to `minecraft:load` and `minecraft:tick` |
| `Namespace.temp` | `temp` | Internal scratch namespace used by helpers |

### The `load` and `tick` Tags

Every namespace automatically has two function tags:

- `ns.load` — functions added here run when the datapack is (re)loaded
- `ns.tick` — functions added here run every game tick

```python
with Namespace("my_pack") as ns:
    with Function(ns / "setup") as setup:
        ~ Say("Datapack loaded!")

    ns.load.add_value(setup)  # register setup to run on /reload
```

> **Tip:** You don't need to manually add these tags to the namespace — they are added automatically. Just add your function to them.

### Singleton Behaviour

Namespaces are **singletons by name**. If you call `Namespace("my_pack")` twice, you get the same object both times. This means you can safely split your code across multiple files and always end up with the correct namespace.

```python
ns_a = Namespace("my_pack")
ns_b = Namespace("my_pack")
assert ns_a is ns_b  # True
```

### Adding Resources to a Namespace

| Method | What it registers |
|--------|------------------|
| `ns.add_function(f)` | A `Function` |
| `ns.add_tag(tag)` | A `Tag` |
| `ns.add_predicate(p)` | A `Predicate` |
| `ns.add_recipe(r)` | A `Recipe` |
| `ns.add_tags(*tags)` | Multiple tags at once |
| `ns.add_recipes(*recipes)` | Multiple recipes at once |

You can also use the generic helper:

```python
ns.add(function_or_tag_or_predicate)
```

### The `with` Statement

Using `with Namespace("my_pack") as ns:` is optional but useful. Inside the block, the namespace is set as "current", which some helpers rely on.

---

## Identifiers

An **Identifier** is the `namespace:path` string Minecraft uses for everything. The `Namespace` class provides a shortcut using the `/` operator:

```python
ns = Namespace("my_pack")

id = ns / "subfolder/my_function"
# equivalent to Identifier.from_string("my_pack:subfolder/my_function")
```

You can also create identifiers directly:

```python
from datagen.utils.minecraft.identifier import Identifier

id = Identifier.of("my_pack:my_function")
```

---

## Functions

A **Function** corresponds to a single `.mcfunction` file.

### Creating a Function

```python
from datagen.function.function import Function

with Namespace("my_pack") as ns:
    with Function(ns / "my_function") as f:
        ~ Say("Hello!")
```

The path after the namespace name maps directly to the folder structure:

| Identifier | File path |
|-----------|-----------|
| `my_pack:greet` | `data/my_pack/function/greet.mcfunction` |
| `my_pack:setup/init` | `data/my_pack/function/setup/init.mcfunction` |

### Adding Commands

Inside a `with Function(...) as f:` block, use the `~` operator:

```python
with Function(ns / "example") as f:
    ~ Say("Line 1")
    ~ Say("Line 2")
    ~ Say("Line 3")
```

Outside a block, use `add_command`:

```python
f = Function(ns / "example")
f.add_command(Say("Line 1"))
f.add_command(Say("Line 2"))
```

### Calling One Function from Another

```python
from datagen.function.commands.runfunction import RunFunction

with Function(ns / "main") as main_fn:
    ~ RunFunction(other_fn)

# Or using the shorthand method:
with Function(ns / "main") as main_fn:
    ~ other_fn.run()
```

### Calling a Function with Macro Arguments

Functions can receive data using Minecraft's macro system:

```python
# With literal values
with Function(ns / "caller") as caller:
    ~ target_fn.run({"player": "Steve", "level": 5})

# With a DataStorage source
from datagen.function.commands._data.datastorage import DataStorage

storage = DataStorage(ns / "__args")
with Function(ns / "caller") as caller:
    ~ storage.set_from_entity("player", TargetSelector.SELF)
    ~ target_fn.run(storage)
```

### Anonymous Functions

`AnonymousFunction` creates a function with an auto-generated name in the `temp` namespace. Use it when you need a one-off function and don't care about its name:

```python
from datagen.function.anonymousfunction import AnonymousFunction

dp = DataPack.get_current_datapack()

with AnonymousFunction(dp) as anon:
    ~ Say("I am anonymous!")

# Use anon.run() to call it from another function
```

---

## Putting It All Together

```python
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.commands.runfunction import RunFunction
from datagen.function.function import Function

def main():
    with DataPack("my_pack", "A complete example") as dp:
        with Namespace("my_pack") as ns:

            with Function(ns / "setup") as setup:
                ~ Say("Pack loaded!")
            ns.load.add_value(setup)

            with Function(ns / "tick") as tick:
                ~ Say("Every tick!")
            ns.tick.add_value(tick)

        dp.add_namespace(ns)
    dp.build()
```

---

## Next Steps

- [Commands →](03-commands.md) — all available command classes
- [Tags & Custom Commands →](04-tags-and-custom-commands.md) — grouping items and blocks
