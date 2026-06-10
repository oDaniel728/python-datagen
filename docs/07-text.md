# Text Components

Minecraft uses **JSON text components** to display rich, formatted text in chat messages, titles, action bars, signs, and more. python-datagen wraps this system in the `Text` class.

> **What are Text Components?**  
> In Minecraft, chat messages, titles, and signs can have coloured text, bold, italic, and even show scoreboard values. This is done with **JSON text components** — a special format the game understands. Instead of writing JSON by hand, you use python-datagen's `Text` class.  
> [Learn more about Text Components on the Minecraft Wiki →](https://minecraft.wiki/w/Text_component)

---

## Import

```python
from datagen.utils.minecraft.text import Text
```

Classes can also be imported directly from their respective submodules:

| Class | Module |
|-------|--------|
| `BaseTextSettings`, `BaseText` | `datagen.utils.minecraft.text._base` |
| `LiteralTextSettings`, `TranslateTextSettings`, `ScoreTextSettings`, `SelectorTextSettings`, `KeybindTextSettings`, `NBTTextSettings` | `datagen.utils.minecraft.text._settings` |
| `literal`, `translate`, `score`, `selector`, `keybind`, `nbt` | `datagen.utils.minecraft.text._components` |

---

## File Structure

```
datagen/utils/minecraft/text/
├── __init__.py       # Text class + re-exports
├── _base.py          # BaseTextSettings, BaseText
├── _settings.py      # *TextSettings classes
└── _components.py    # literal, translate, score, selector, keybind, nbt
```

---

## Text Types

There are six types of text components. All of them are subclasses of `Text.BaseText` and can be passed to commands like `Tellraw`, `Title`, `Scoreboard`, etc.

---

### `Text.literal` — plain text

The most common type. Displays a fixed string.

```python
Text.literal("Hello, world!")
```

With formatting:

```python
settings = Text.LiteralTextSettings(
    bold=True,
    color="gold"
)
Text.literal("Important!", settings)
```

---

### `Text.translate` — translatable text

Displays a localization key. Minecraft replaces it with the player's language translation.

```python
Text.translate(Identifier.of("item.minecraft.diamond"))
```

With a fallback for when the key doesn't exist:

```python
settings = Text.TranslateTextSettings(
    translate=Identifier.of("my_pack.some_key"),
    fallback="Default text"
)
Text.of(settings)
```

---

### `Text.score` — scoreboard value

Displays the value of a scoreboard objective for a player.

```python
from datagen.utils.scoreboard.player import ScoreboardPlayer

player = my_objective.player(TargetSelector.SELF)
Text.score(player)
```

---

### `Text.selector` — entity name

Displays the name(s) of entities matching a selector.

```python
Text.selector(TargetSelector.NEAREST_PLAYER)
# In-game: displays the nearest player's name
```

---

### `Text.keybind` — key binding

Displays the name of a key binding (e.g. "W" for forward).

```python
from datagen.utils.repr.keybind import KeyBind

Text.keybind(KeyBind.FORWARD)
```

---

### `Text.nbt` — NBT data

Displays a value from entity, block, or storage NBT.

```python
Text.nbt("Health", source="entity")
```

---

## Formatting Options

All text types accept a settings object with these optional parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bold` | `bool` | `False` | Bold text |
| `italic` | `bool` | `False` | Italic text |
| `underlined` | `bool` | `False` | Underlined text |
| `strikethrough` | `bool` | `False` | Strikethrough text |
| `obfuscated` | `bool` | `False` | Randomly scrambled characters |
| `color` | `str` | `"white"` | Named color or hex string |
| `font` | `Identifier \| None` | `None` | Custom font identifier |

### Named Colors

```
"black"       "dark_blue"    "dark_green"
"dark_aqua"   "dark_red"     "dark_purple"
"gold"        "gray"         "dark_gray"
"blue"        "green"        "aqua"
"red"         "light_purple" "yellow"
"white"
```

You can also pass a hex color string:

```python
Text.LiteralTextSettings(color="#FF4500")
```

---

## Using `Text.of` (Settings-Based Creation)

`Text.of` accepts a settings object and returns the correct text type automatically:

```python
msg = Text.of(Text.LiteralTextSettings(
    text="Hello!",
    bold=True,
    color="green"
))
```

---

## Practical Examples

### Tellraw with formatted text

```python
from datagen.function.commands.tellraw import Tellraw

~ Tellraw(
    TargetSelector.ALL_PLAYERS,
    Text.literal("Welcome to the server!", Text.LiteralTextSettings(bold=True, color="gold"))
)
```

### Title with subtitle

```python
from datagen.function.commands.title import Title

~ Title.title(
    TargetSelector.ALL_PLAYERS,
    Text.literal("Round Over", Text.LiteralTextSettings(bold=True, color="red"))
)
~ Title.subtitle(
    TargetSelector.ALL_PLAYERS,
    Text.literal("You lost!", Text.LiteralTextSettings(color="dark_red"))
)
```

### Scoreboard display name

```python
from datagen.function.commands.scoreboard import Scoreboard

obj = Scoreboard.objective(
    "kills",
    Text.literal("Kill Count", Text.LiteralTextSettings(color="red", bold=True)),
)
~ obj.add()
```

### Show player's score in chat

```python
player = obj.player(TargetSelector.SELF)
~ Tellraw(
    TargetSelector.SELF,
    Text.score(player, Text.ScoreTextSettings(color="aqua"))
)
```

---

## Converting to String / Dict

All `Text.BaseText` objects can be serialized:

```python
msg = Text.literal("Hello!")
msg.to_string()  # '{"text": "Hello!"}'
msg.to_dict()    # {"text": "Hello!"}
```

This is done automatically when you pass a `Text` object to a command.

---

## Next Steps

- [Recipes →](08-recipes.md)
- [Predicates →](09-predicates.md)
