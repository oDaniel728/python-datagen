# Getting Started

Welcome! This guide will walk you through everything you need to know to set up the project and create your first Minecraft datapack using python-datagen.

---

## Prerequisites

- **Python 3.12+** installed on your system
- Basic familiarity with Python (you don't need to be an expert)
- A code editor (VS Code is recommended)

---

## Project Layout

When you clone or download the project, you will see this structure:

```
my-project/
├── .datagenconfig       ← configuration file (output paths, etc.)
├── __main__.py          ← entry point, runs src/main.py
├── src/
│   └── main.py          ← YOUR code goes here
├── datapacks/           ← generated datapacks appear here
├── datagen/             ← the library (do not edit)
└── datagenpp/           ← extended helpers built on top of datagen
```

You will only need to edit files inside `src/`.

---

## Running the Project

From the project root, run:

```bash
python .
```

This calls `__main__.py`, which imports and runs `src/main.py`. After running, the output datapack folder will appear inside `datapacks/` (or wherever `output` is set in `.datagenconfig`).

---

## Your First Datapack

Open `src/main.py` and replace its contents with the following:

```python
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function

def main():
    # 1. Create a DataPack
    with DataPack("hello_world", "My first datapack") as dp:

        # 2. Create a Namespace (same name as the datapack is common)
        with Namespace("hello_world") as ns:

            # 3. Create a Function inside the namespace
            with Function(ns / "greet") as f:
                ~ Say("Hello, world!")

        # 4. Register the namespace with the datapack
        dp.add_namespace(ns)

    # 5. Build — writes all files to disk
    dp.build()
```

Run `python .` and check `datapacks/hello_world/`. You should see:

```
hello_world/
├── pack.mcmeta
└── data/
    └── hello_world/
        └── function/
            └── greet.mcfunction
```

The file `greet.mcfunction` will contain:

```
say Hello, world!
```

---

## What Each Step Does

| Step | What it does |
|------|-------------|
| `DataPack("hello_world", "My first datapack")` | Declares a new datapack with a name and a description shown in-game |
| `Namespace("hello_world")` | Creates a namespace — all functions and tags live inside one |
| `Function(ns / "greet")` | Creates a `.mcfunction` file at `hello_world:greet` |
| `~ Say("Hello, world!")` | Adds the `say` command to the function (the `~` operator does the adding) |
| `dp.add_namespace(ns)` | Links the namespace to the datapack so it gets built |
| `dp.build()` | Writes everything to disk |

---

## The `~` Operator

When you are inside a `with Function(...) as f:` block, using `~ SomeCommand(...)` automatically appends that command to the current function. This is the primary way to add commands.

You can also add commands explicitly without the `with` block:

```python
f = Function(ns / "greet")
f.add_command(Say("Hello, world!"))
```

Both styles produce identical output.

---

## Next Steps

- [Namespaces & Functions →](02-namespaces-and-functions.md) — learn about organizing your code
- [Commands →](03-commands.md) — see all available command classes
