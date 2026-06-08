# Configuration — `.datagenconfig`

The `.datagenconfig` file is a JSON file in the root of your project that controls where the library reads from and writes to. It is loaded automatically when any part of `datagen` is imported.

---

## File Location

```
my-project/
├── .datagenconfig   ← must be here, in the project root
├── __main__.py
├── src/
└── ...
```

> **Important:** The library reads `.datagenconfig` relative to the working directory. Always run your project from the project root (`python .`), not from inside a subdirectory.

---

## Default Contents

```json
{
    "builderSettings": {
        "source": "src/",
        "output": "datapacks/",
        "indent": 4
    },
    "dumperSettings": {
        "source": "dumpgen/dumps/",
        "output": "datagen/utils/minecraft/collections/"
    }
}
```

---

## Settings Reference

### `builderSettings`

These settings control how your datapack is built.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `source` | `string` | `"src/"` | The folder containing your `main.py` entry point. |
| `output` | `string` | `"datapacks/"` | The folder where built datapacks will be written. |
| `indent` | `int` | `4` | JSON indentation width used in generated files. |

#### `source`

The `source` folder is where `__main__.py` looks for `main.py`. If you want to organize your code differently, change this path:

```json
"source": "my_source/"
```

Make sure the folder contains a `main.py` with a `main()` function.

#### `output`

All datapacks built with `dp.build()` are placed here. For example, if `output` is `"datapacks/"` and your datapack name is `"my_pack"`, the result will be at:

```
datapacks/my_pack/
├── pack.mcmeta
└── data/
    └── ...
```

You can point this directly to your Minecraft world's `datapacks/` folder for rapid iteration:

```json
"output": "/home/yourname/.minecraft/saves/MyWorld/datapacks/"
```

#### `indent`

Controls the JSON indentation in all output files (`pack.mcmeta`, tag files, recipe files, etc.):

```json
"indent": 2
```

---

### `dumperSettings`

These settings are only used by DumpGen (`python dumpgen/gen.py`). They do not affect normal datapack building.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `source` | `string` | `"dumpgen/dumps/"` | Folder containing the raw Minecraft JSON dump files. |
| `output` | `string` | `"datagen/utils/minecraft/collections/"` | Folder where generated Python constant files are written. |

---

## Example: Point Output to a Minecraft World

```json
{
    "builderSettings": {
        "source": "src/",
        "output": "/home/yourname/.minecraft/saves/MyWorld/datapacks/",
        "indent": 4
    },
    "dumperSettings": {
        "source": "dumpgen/dumps/",
        "output": "datagen/utils/minecraft/collections/"
    }
}
```

Now running `python .` will write the datapack directly into your Minecraft world. Use `/reload` in-game to apply the changes.

---

## Accessing Config in Code

If you need to read config values programmatically:

```python
from datagen.globals import DatagenConfig

output_dir = DatagenConfig.config["builderSettings"]["output"]
```

---

## Back to Top

- [README →](../readme.md)
- [Getting Started →](01-getting-started.md)
