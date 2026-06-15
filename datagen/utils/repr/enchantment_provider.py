from typing import Literal, Self

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._base import BaseText, _remove_nulls
from datagen.utils.simplefile import SimpleFile


class EnchantmentProvider(ToDict):
    """
    # EnchantmentProvider
    - See https://minecraft.wiki/w/Enchantment_definition

    ## Summary
    Creates a custom Minecraft enchantment with its own name, behavior, and effects.

    Think of this as a "blueprint" for a new enchantment. You can make enchantments
    that do almost anything: extra damage, potion effects, explosions, run commands,
    prevent item loss, and much more.

    ## How it works
    1. Create an `EnchantmentProvider` with a unique ID (like `"mypack:thunder"`)
    2. Use `.with_*()` methods to configure it (name, items, effects, etc.)
    3. Use `~enchantment` to register it in its namespace
    4. Add the namespace to your datapack and build

    ## Examples

    ### Simple damage enchantment
    ```python
    from datagen.utils.repr.enchantment_provider import EnchantmentProvider
    from datagen.utils.repr.enchantmenteffects import ValueEffect
    from datagen.utils.repr.levelbasedvalue import LevelBasedValue
    from datagen.utils.minecraft.text import Text
    from datagen.utils.minecraft.identifier import Identifier

    sharpness = EnchantmentProvider(Identifier.of("mypack:super_sharp"))
    sharpness \\
        .with_description(Text.literal("Super Sharp")) \\
        .with_max_level(5) \\
        .with_weight(10) \\
        .with_supported_items("minecraft:diamond_sword") \\
        .with_anvil_cost(3) \\
        .with_cost(1, 10, 15, 10) \\
        .with_slots("mainhand") \\
        .with_value_effect(
            "minecraft:damage",
            ValueEffect.add(LevelBasedValue.linear(2.0, 1.0))
        )
    ~sharpness
    ```

    ### Enchantment with entity effects
    ```python
    frost = EnchantmentProvider(Identifier.of("mypack:frost_aura"))
    frost \\
        .with_description(Text.literal("Frost Aura")) \\
        .with_max_level(2) \\
        .with_supported_items("minecraft:diamond_chestplate") \\
        .with_anvil_cost(4) \\
        .with_cost(15, 10, 30, 10) \\
        .with_slots("chest") \\
        .with_entity_effect(
            "minecraft:post_attack",
            EntityEffect.apply_mob_effect(
                to_apply=["minecraft:slowness"],
                min_duration=LevelBasedValue.linear(2, 1),
                max_duration=LevelBasedValue.linear(4, 2),
                min_amplifier=0,
                max_amplifier=1
            ),
            enchanted="attacker",
            affected="victim"
        )
    ~frost
    ```

    ### Utility enchantment (runs a function every tick)
    ```python
    feeder = EnchantmentProvider(Identifier.of("mypack:auto_feeder"))
    feeder \\
        .with_description(Text.literal("Auto Feeder")) \\
        .with_max_level(1) \\
        .with_weight(1) \\
        .with_supported_items("minecraft:netherite_helmet") \\
        .with_anvil_cost(5) \\
        .with_slots("head") \\
        .with_entity_effect(
            "minecraft:tick",
            EntityEffect.run_function("mypack:auto_feed"),
            enchanted="this",
            affected="this"
        )
    ~feeder
    ```
    """

    def __init__(self, id: Identifier):
        """
        Creates a new enchantment blueprint with the given identifier.

        The identifier determines the enchantment's registry name (e.g. `"mypack:thunder"`)
        and which namespace it belongs to.
        """
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.get(id)
        self._data: dict = {}

    # --- Basic properties ---

    def with_description(self, description: str | BaseText) -> Self:
        """
        Sets the enchantment's name/tooltip shown in the game.

        You can pass a simple text or a formatted `BaseText` for colors and styles.
        This is the name players will see in the enchanting table, anvil, and item tooltips.

        ## Examples

        ### Simple name
        ```python
        .with_description(Text.literal("Super Sharp"))
        ```

        ### Colored name
        ```python
        .with_description(Text.literal("Frost Aura", Text.LiteralTextSettings(color="aqua")))
        ```

        ### Translated name (uses the game's language file)
        ```python
        .with_description(Text.translate(Identifier.of("enchantment.mypack.thunder")))
        ```
        """
        if isinstance(description, BaseText):
            self._data["description"] = _remove_nulls(description.to_dict())
        else:
            self._data["description"] = description
        return self

    def with_exclusive_set(self, *enchantments: str | Identifier) -> Self:
        """
        Marks other enchantments as incompatible with this one.

        If an item already has one of these enchantments, this enchantment
        cannot be applied (and vice versa). This is how Minecraft prevents
        Sharpness + Smite on the same sword.

        ## Example
        ```python
        .with_exclusive_set(
            str(Enchantments.SHARPNESS),
            str(Enchantments.SMITE),
        )
        ```
        """
        self._data["exclusive_set"] = [str(e) for e in enchantments]
        return self

    def with_supported_items(self, *items: str | Identifier) -> Self:
        """
        Sets which items can receive this enchantment.

        Only items listed here can have this enchantment applied through
        enchanting tables, anvils, or commands. Each item is its Minecraft
        registry ID like `"minecraft:diamond_sword"`.

        ## Example
        ```python
        .with_supported_items(
            "minecraft:diamond_sword",
            "minecraft:netherite_sword",
            "minecraft:iron_axe",
        )
        ```
        """
        self._data["supported_items"] = [str(i) for i in items]
        return self

    def with_primary_items(self, *items: str | Identifier) -> Self:
        """
        Sets which items can get this enchantment from the enchanting table.

        If an item is in `supported_items` but NOT in `primary_items`, it can
        only receive the enchantment through an anvil or commands, not the
        enchanting table. Useful for making "treasure-only" enchantments
        like Mending available on certain items.

        ## Example
        ```python
        .with_supported_items("minecraft:diamond_sword", "minecraft:stick") \\
        .with_primary_items("minecraft:diamond_sword")
        # Stick can get it via anvil, diamond sword via enchanting table too
        ```
        """
        self._data["primary_items"] = [str(i) for i in items]
        return self

    def with_weight(self, weight: int) -> Self:
        """
        Sets how likely this enchantment is to appear in the enchanting table.

        Higher weight = more common. Sharpness has weight 10, Frost Walker has weight 2.
        If you want your enchantment to be rare, use a low number like 1 or 2.

        ## Example
        ```python
        .with_weight(5)  # moderately common
        ```
        """
        self._data["weight"] = weight
        return self

    def with_max_level(self, level: int) -> Self:
        """
        Sets the maximum level this enchantment can reach.

        For example, Sharpness has max_level 5, Fortune has max_level 3.
        This is the highest level obtainable through the enchanting table or anvil.

        ## Example
        ```python
        .with_max_level(3)  # enchantment goes up to level III
        ```
        """
        self._data["max_level"] = level
        return self

    def with_cost(self, min_base: int, min_per_level: int, max_base: int, max_per_level: int) -> Self:
        """
        Sets the minimum and maximum enchanting cost at each level.

        The actual cost shown in the enchanting table is calculated as:
        - Min cost = `min_base + min_per_level * (level - 1)`
        - Max cost = `max_base + max_per_level * (level - 1)`

        Higher costs make the enchantment harder/expensive to obtain.

        ## Example
        ```python
        # Level 1: 10-25, Level 2: 15-35, Level 3: 20-45
        .with_cost(10, 5, 25, 10)
        ```
        """
        self._data["min_cost"] = {"base": min_base, "per_level_above_first": min_per_level}
        self._data["max_cost"] = {"base": max_base, "per_level_above_first": max_per_level}
        return self

    def with_anvil_cost(self, cost: int) -> Self:
        """
        Sets the extra anvil cost for combining/repairing items with this enchantment.

        This is added on top of the regular anvil repair cost. Higher values
        make it more expensive to combine books or apply the enchantment in an anvil.

        ## Example
        ```python
        .with_anvil_cost(3)  # cheap to combine
        .with_anvil_cost(8)  # expensive to combine (treasure enchantment)
        ```
        """
        self._data["anvil_cost"] = cost
        return self

    _TSlot = Literal[
        "mainhand", "offhand", "head", "chest", "legs", "feet", "hand", "armor"
    ]
    def with_slots(self, *slots: _TSlot) -> Self:
        """
        Sets which equipment slots activate this enchantment's effects.

        Available slots: `"mainhand"`, `"offhand"`, `"head"`, `"chest"`,
        `"legs"`, `"feet"`, `"hand"` (both hands), `"armor"` (all armor).

        Effects like `minecraft:tick` run on the item in these slots.
        Effects like `minecraft:post_attack` trigger when the entity wearing
        the item attacks or is attacked.

        ## Example
        ```python
        .with_slots("mainhand")           # weapon enchantment
        .with_slots("chest")              # chestplate enchantment
        .with_slots("head", "chest", "legs", "feet")  # all armor
        ```
        """
        self._data["slots"] = list(slots)
        return self

    # --- Effects ---

    def with_effect(self, component_id: str, *entries: dict) -> Self:
        """
        Adds raw effect entries to an effect component.

        This is a low-level method for advanced users who know the Minecraft
        enchantment JSON format. Most users should use `with_value_effect`,
        `with_entity_effect`, or the specialized helper methods instead.

        ## Example
        ```python
        .with_effect("minecraft:damage", [
            {"effect": {"type": "minecraft:add", "value": 5.0}}
        ])
        ```
        """
        if "effects" not in self._data:
            self._data["effects"] = {}
        if component_id not in self._data["effects"]:
            self._data["effects"][component_id] = []
        self._data["effects"][component_id].extend(entries)
        return self

    def with_value_effect(self, component_id: str, effect: ToDict, requirements: dict | None = None, enchanted: str | None = None) -> Self:
        """
        Adds a value effect to the enchantment.

        Value effects modify numbers: damage, knockback, armor, movement speed, etc.
        The `component_id` determines what is being modified (like `"minecraft:damage"`).

        ## Example
        ```python
        .with_value_effect(
            "minecraft:damage",
            ValueEffect.add(LevelBasedValue.linear(2.0, 1.0))
        )
        # Adds 2 + level damage
        ```
        """
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        return self.with_effect(component_id, EffectComponent.value_component(effect, requirements, enchanted))

    def with_entity_effect(self, component_id: str, effect: ToDict, enchanted: str, affected: str, requirements: dict | None = None) -> Self:
        """
        Adds an entity effect to the enchantment.

        Entity effects do things to entities: apply potions, deal damage,
        spawn particles, run functions, summon mobs, ignite, explode, etc.
        The `enchanted` and `affected` parameters control who does what to whom.

        ## Parameters

        - `enchanted`: The role of the entity wearing the enchanted item
          (`"attacker"`, `"victim"`, `"this"`, `"damager"`)
        - `affected`: The role of the entity being affected
          (`"attacker"`, `"victim"`, `"this"`, `"damager"`)

        ## Example
        ```python
        .with_entity_effect(
            "minecraft:post_attack",
            EntityEffect.ignite(LevelBasedValue.linear(2, 1)),
            enchanted="attacker",
            affected="victim",
        )
        # When attacker hits victim, victim burns for 2 + level seconds
        ```
        """
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        return self.with_effect(component_id, EffectComponent.entity_component(effect, enchanted, affected, requirements))

    def with_attributes(self, *attributes: ToDict) -> Self:
        """
        Adds attribute modifiers to the enchantment.

        These work like item attribute modifiers, modifying the wearer's
        stats (attack damage, movement speed, armor, knockback resistance, etc.).

        ## Example
        ```python
        from datagen.utils.repr.enchantmenteffects import AttributeEffect

        .with_attributes(
            AttributeEffect("minecraft:generic.attack_damage",
                id="mypack:super_sharp",
                amount=LevelBasedValue.linear(2.0, 1.0),
                operation="add_value",
            )
        )
        ```
        """
        self._data["effects"] = self._data.get("effects", {})
        if "minecraft:attributes" not in self._data["effects"]:
            self._data["effects"]["minecraft:attributes"] = []
        for attr in attributes:
            self._data["effects"]["minecraft:attributes"].append(_remove_nulls(attr.to_dict()) if hasattr(attr, "to_dict") else _remove_nulls(attr))
        return self

    def with_damage_immunity(self, requirements: dict | None = None) -> Self:
        """
        Makes the wearer immune to specific damage types.

        When combined with a `requirements` condition, you can make the
        wearer immune only under certain circumstances.

        ## Example
        ```python
        # Immune to all damage while wearing this item
        .with_damage_immunity()

        # Immune to fall damage only
        .with_damage_immunity({
            "condition": "minecraft:damage_source_properties",
            "predicate": {"tags": [{"id": "minecraft:is_fall", "expected": True}]}
        })
        ```
        """
        entry: dict = {"effect": {}}
        if requirements is not None:
            entry["requirements"] = requirements
        return self.with_effect("minecraft:damage_immunity", _remove_nulls(entry))

    def with_prevent_equipment_drop(self) -> Self:
        """
        Prevents the item from being dropped on death.

        Perfect for "soulbound" enchantments that keep your favorite
        gear safe when you die. The item stays in the inventory after death.

        ## Example
        ```python
        .with_prevent_equipment_drop()
        ```
        """
        return self.with_effect("minecraft:prevent_equipment_drop", {})

    def with_prevent_armor_change(self) -> Self:
        """
        Prevents the armor piece from being removed from its slot.

        The player cannot take off this armor piece until the enchantment
        is removed. Useful for cursed/locked items in adventure maps.

        ## Example
        ```python
        .with_prevent_armor_change()
        ```
        """
        return self.with_effect("minecraft:prevent_armor_change", {})

    def with_location_changed(self, effect: ToDict, requirements: dict | None = None) -> Self:
        """
        Runs an effect when the wearer moves to a different location.

        This triggers when the entity changes blocks. Combined with
        requirements, you can create effects that only happen in specific
        biomes, dimensions, or light levels.

        ## Example
        ```python
        .with_location_changed(
            EntityEffect.spawn_particles(
                "minecraft:heart_particle",
                LevelBasedValue.constant(1)
            ),
            requirements={
                "condition": "minecraft:location_check",
                "predicate": {
                    "biomes": "minecraft:plains"
                }
            }
        )
        ```
        """
        from datagen.utils.repr.enchantmenteffects import EffectComponent
        entry: dict = {"effect": effect.to_dict() if hasattr(effect, "to_dict") else effect}
        if requirements is not None:
            entry["requirements"] = requirements
        return self.with_effect("minecraft:location_changed", entry)

    def with_crossbow_charge_sounds(self, *levels: dict) -> Self:
        """
        Sets custom sounds for each crossbow charge level.

        Each level dict should contain `start`, `end`, and optionally
        `sound` fields. This only works on crossbow enchantments.

        ## Example
        ```python
        .with_crossbow_charge_sounds(
            {"start": 0.0, "end": 0.5, "sound": "minecraft:entity.arrow.shoot"},
            {"start": 0.5, "end": 1.0},
        )
        ```
        """
        return self.with_effect("minecraft:crossbow_charge_sounds", *levels)

    def with_trident_sound(self, *sounds: str) -> Self:
        """
        Sets custom sounds for the trident when this enchantment is applied.

        The format expects sound definition dictionaries with volume, pitch, etc.

        ## Example
        ```python
        .with_trident_sound(
            {"sound": "minecraft:entity.lightning_bolt.thunder", "volume": 2.0}
        )
        ```
        """
        return self.with_effect("minecraft:trident_sound", *[_remove_nulls(sound) for sound in sounds]) # type: ignore

    # --- Serialization ---

    def get_filepath(self) -> str:
        """
        Returns the file path where this enchantment's JSON file will be saved.

        The path is relative to the namespace data directory, in the
        `enchantment/` folder (e.g. `data/mypack/enchantment/thunder.json`).
        """
        return f"enchantment/{self.id._path}.json"

    def to_dict(self) -> dict:
        """
        Converts this enchantment to a dictionary, ready for JSON serialization.

        The dictionary follows Minecraft's enchantment definition format and
        is what gets written to the JSON file during datapack building.
        """
        return dict(self._data)

    def to_file(self) -> SimpleFile:
        """
        Converts this enchantment to a `SimpleFile` for writing to disk.

        Called automatically during `dp.build()`. You usually don't need to
        call this directly.
        """
        import json
        return SimpleFile(self.get_filepath(), json.dumps(self.to_dict(), indent=4))

    # --- Auto-registration ---

    def __invert__(self) -> Self:
        """
        Registers this enchantment in its namespace.

        The `~enchantment` syntax is a shortcut for adding the enchantment
        to its namespace, just like how `~function` registers a function
        or adds a command to the active function.

        ## Example
        ```python
        thunder = EnchantmentProvider(Identifier.of("mypack:thunder"))
        thunder \\
            .with_description(Text.literal("Thunder")) \\
            .with_max_level(3)
        ~thunder  # registers in 'mypack' namespace
        ```
        """
        self.namespace.add_enchantment(self)
        return self
