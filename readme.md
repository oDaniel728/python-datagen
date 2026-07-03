# python-datagen

A Python library for generating Minecraft Java Edition datapacks programmatically. Instead of writing `.mcfunction` files by hand, you describe your datapack logic in Python — the library handles file structure, command formatting, and everything else.

---

## Features

- Create datapacks, namespaces, and functions in pure Python
- Full command coverage (`say`, `execute`, `scoreboard`, `give`, `teleport`, and many more)
- Tag support for items, blocks, and functions
- Text component builder (`Text.literal`, `Text.translate`, colors, formatting)
- Scoreboard objective helpers
- `Script` and `ScriptBuilder` for high-level game event hooks
- `DumpGen` to regenerate Minecraft data constants from game dumps
- Configurable via `datagen.json`

---

## Quick Start

```python
# src/main.py
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.function import Function

def main():
    with DataPack("my_pack", "My first datapack") as dp:
        with Namespace("my_pack") as ns:
            with Function(ns / "hello") as f:
                ~ Say("Hello, world!")
        dp.add_namespace(ns)
    dp.build()
```

Run with:

```bash
python .
```

The generated datapack will be placed in the folder configured in `datagen.json` (default: `datapacks/`).

---

## Documentation

| Page | Topic |
|------|-------|
| [Getting Started](docs/01-getting-started.md) | Installation, project layout, first datapack |
| [Namespaces & Functions](docs/02-namespaces-and-functions.md) | Organizing your datapack |
| [Commands](docs/03-commands.md) | All available command classes |
| [Tags & Custom Commands](docs/04-tags-and-custom-commands.md) | Function/item/block tags and raw commands |
| [Target Selectors](docs/05-target-selectors.md) | `@s`, `@a`, `@e` and filters |
| [Execute](docs/06-execute.md) | The `execute` command builder |
| [Text Components](docs/07-text.md) | Rich text for `tellraw`, titles, etc. |
| [Recipes](docs/08-recipes.md) | Crafting recipe definitions |
| [Predicates](docs/09-predicates.md) | Loot/condition predicates *(experimental)* |
| [Script & ScriptBuilder](docs/10-script-and-scriptbuilder.md) | High-level event hooks |
| [DumpGen](docs/11-dumpgen.md) | Regenerating game data constants |
| [Configuration](docs/12-configuration.md) | `datagen.json` reference |
| [Advancements](docs/13-advancements.md) | Advancement definitions |
| [Enums & Collections](docs/14-enums.md) | Minecraft data constants |

---

## License

See [LICENSE](LICENSE).
