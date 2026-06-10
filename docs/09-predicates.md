# Predicates

> **What are Predicates?**  
> Predicates are condition files in Minecraft. They test things like "is the player holding a diamond?", "is the entity on fire?", "is it night?". You use predicates in commands (`/execute if predicate`), loot tables, and advancements.  
> [Learn more about Predicates on the Minecraft Wiki →](https://minecraft.wiki/w/Predicate)

> ⚠️ **Experimental — use with caution.**
> The predicate system is functional but incomplete. The builder utilities and ID management are rough, and the API may change significantly in future versions. For complex predicates, passing a raw dict is often more reliable than using the helpers.

---

## Import

```python
from datagen.predicate.predicate import Predicate
from datagen.utils.minecraft.identifier import Identifier
```

---

## Creating a Predicate

The `Predicate` class takes an identifier and a raw dict that matches the Minecraft predicate JSON format:

```python
on_fire = Predicate(
    Identifier.of("my_pack:is_on_fire"),
    {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {
            "flags": {
                "is_on_fire": True
            }
        }
    }
)
```

Predicates are automatically registered with their namespace (based on the identifier's namespace). You don't need to call `ns.add_predicate()` explicitly.

---

## Using a Predicate in Execute

```python
from datagen.function.commands.execute import Execute

Execute().IF(lambda b: b.predicate(on_fire)).RUN(Say("You are on fire!"))
# → execute if predicate my_pack:is_on_fire run say You are on fire!
```

---

## Default Namespace

By default, newly created `Predicate` objects register themselves into `Namespace.temp`. To change this, call:

```python
Predicate.use_namespace(ns)
```

All `Predicate` objects created after this call will be registered in `ns`.

---

## Common Predicate Conditions

Below are some of the most common Minecraft predicate conditions written as raw dicts. The full list is in the [Minecraft Wiki — Predicate](https://minecraft.wiki/w/Predicate).

### Entity is on fire

```python
Predicate(Identifier.of("my_pack:is_on_fire"), {
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {"flags": {"is_on_fire": True}}
})
```

### Player is sneaking

```python
Predicate(Identifier.of("my_pack:is_sneaking"), {
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {"flags": {"is_sneaking": True}}
})
```

### Entity is a specific type

```python
Predicate(Identifier.of("my_pack:is_zombie"), {
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {"type": "minecraft:zombie"}
})
```

### Player holds a specific item (main hand)

```python
Predicate(Identifier.of("my_pack:holds_diamond"), {
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {
        "equipment": {
            "mainhand": {"items": "minecraft:diamond"}
        }
    }
})
```

### Random chance (50%)

```python
Predicate(Identifier.of("my_pack:fifty_percent"), {
    "condition": "minecraft:random_chance",
    "chance": 0.5
})
```

### Inverted condition

```python
Predicate(Identifier.of("my_pack:not_on_fire"), {
    "condition": "minecraft:inverted",
    "term": {
        "condition": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {"flags": {"is_on_fire": True}}
    }
})
```

### All conditions must pass

```python
Predicate(Identifier.of("my_pack:sneaking_and_on_fire"), {
    "condition": "minecraft:all_of",
    "terms": [
        {
            "condition": "minecraft:entity_properties",
            "entity": "this",
            "predicate": {"flags": {"is_sneaking": True}}
        },
        {
            "condition": "minecraft:entity_properties",
            "entity": "this",
            "predicate": {"flags": {"is_on_fire": True}}
        }
    ]
})
```

---

## Output

Each predicate is written to `data/<namespace>/predicate/<path>.json` when you call `dp.build()`.

---

## Next Steps

- [Script & ScriptBuilder →](10-script-and-scriptbuilder.md)
