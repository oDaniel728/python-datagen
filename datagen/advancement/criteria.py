from typing import Any, Iterable, NotRequired, TypedDict

from datagen.predicate.predicate import Predicate
from datagen.types.util.counter import Counter
from datagen.types.util.min import Range
from datagen.types.util.validpredicate import ValidPredicate
from datagen.utils._dictify import dictify
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.biome import Biome
from datagen.utils.repr.block import Block
from datagen.utils.repr.damagesourcepredicate import DamageSourcePredicate
from datagen.utils.repr.dimension import Dimension
from datagen.utils.repr.entitypredicate import EntityPredicate
from datagen.utils.repr.item import Item
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.locationpredicate import LocationPredicate
from datagen.utils.repr.status_effect import StatusEffect

_c = Counter()
class Criteria():
    def __init__(
        self, 
        name: str = "main", 
        require: bool = True, 
        data: dict[str, Any] | None = None
    ) -> None:
        self.name = name
        self.required = require
        self.data = data if data is not None else {}

    def set_name(self, value: str) -> "Criteria":
        self.name = value
        return self
    
    def set_required(self, value: bool) -> "Criteria":
        self.required = value
        return self
    
    def set_data(self, value: dict[str, Any]) -> "Criteria":
        self.data = value
        return self

    @staticmethod
    def allay_drop_item_on_block(
        location: LocationPredicate,
        item: ItemPredicate | None = None
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:allay_drop_item_on_block"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["location"] = location.to_dict()
        if item is not None:
            conditions["item"] = item.to_dict()

        return Criteria(
            name = f"allay_drop_item_on_block_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def any_block_use(
        *predicates: Predicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:any_block_use"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["location"] = [predicate.to_dict() for predicate in predicates]

        return Criteria(
            name = f"any_block_use_{_c.get()}",
            data = data
        )

    @staticmethod
    def bee_nest_destroyed(
        block: Block,
        item: ItemPredicate,
        num_bees_inside: int | Range
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:bee_nest_destroyed"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["block"] = str(block.id)
        conditions["item"] = item.to_dict()
        if isinstance(num_bees_inside, int):
            conditions["num_bees_inside"] = num_bees_inside
        else:
            conditions["num_bees_inside"] = {"min": num_bees_inside.start, "max": num_bees_inside.end}

        return Criteria(
            name = f"bee_nest_destroyed_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def bred_animals(
        child: EntityPredicate,
        parent: EntityPredicate,
        partner: EntityPredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:bred_animals"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["child"] = child.to_dict()
        conditions["parent"] = parent.to_dict()
        conditions["partner"] = partner.to_dict()

        return Criteria(
            name = f"bred_animals_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def brewed_potion(
        potion: Identifier
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:brewed_potion"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["potion"] = str(potion)

        return Criteria(
            name = f"brewed_potion_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def changed_dimension(
        from_: Dimension | None = None,
        to: Dimension | None = None
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:changed_dimension"
        data["conditions"] = {}
        conditions = data["conditions"]
        if from_ is not None:
            conditions["from"] = str(from_)
        if to is not None:
            conditions["to"] = str(to)

        return Criteria(
            name = f"changed_dimension_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def construct_beacon(
        level: int | Range
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:construct_beacon"
        data["conditions"] = {}
        conditions = data["conditions"]
        if isinstance(level, int):
            conditions["level"] = level
        else:
            conditions["level"] = {"min": level.start, "max": level.end}

        return Criteria(
            name = f"construct_beacon_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def consume_item(
        item: ItemPredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:consume_item"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = item.to_dict()

        return Criteria(
            name = f"consume_item_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def default_block_use(
        *predicates: Predicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:default_block_use"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["location"] = [predicate.to_dict() for predicate in predicates]

        return Criteria(
            name = f"default_block_use_{_c.get()}",
            data = data
        )
    
    class _TRange(TypedDict):
        min: NotRequired[int]
        max: NotRequired[int]
    class _TEffect(TypedDict):
        amplifier: NotRequired[int | EntityPredicate._TRange | Range]
        duration: NotRequired[int | EntityPredicate._TRange | Range]
        ambient: NotRequired[bool]
        visible: NotRequired[bool]
    @staticmethod
    def effects_changed(
        effects: dict[StatusEffect, _TEffect],
        source: EntityPredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:effects_changed"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["effects"] = {str(effect.id): effect_data for effect, effect_data in effects.items()}
        conditions["source"] = source.to_dict()

        return Criteria(
            name = f"effects_changed_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def enchanted_item(
        item: ItemPredicate,
        levels: int | Range | None = None,
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:enchanted_item"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = item.to_dict()
        if levels is not None:
            if isinstance(levels, int):
                conditions["levels"] = levels
            else:
                conditions["levels"] = {"min": levels.start, "max": levels.end}

        return Criteria(
            name = f"enchanted_item_{_c.get()}",
            data = data
        )

    @staticmethod
    def enter_block(
        block: Block,
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:enter_block"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["block"] = str(block.id)
        conditions["state"] = dictify(block.settings.get_block_state()) # type: ignore

        return Criteria(
            name = f"enter_block_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def entity_killed_player(
        entity: EntityPredicate,
        killing_blow: DamageSourcePredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:entity_killed_player"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["entity"] = entity.to_dict()
        conditions["killing_blow"] = killing_blow.to_dict()

        return Criteria(
            name = f"entity_killed_player_{_c.get()}",
            data = data
        )
    
    # TODO: fall_after_explosion
    
    @staticmethod
    def filled_bucket(
        item: ItemPredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:filled_bucket"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = item.to_dict()

        return Criteria(
            name = f"filled_bucket_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def impossible() -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:impossible"
        data["conditions"] = {}

        return Criteria(
            name = f"impossible_{_c.get()}",
            data = data
        )
    
    _TSlots = TypedDict("_TSlots", {
        "empty": NotRequired[int | Range],
        "full": NotRequired[int | Range],
        "occupied": NotRequired[int | Range]
    })
    @staticmethod
    def inventory_changed(
        *items: ItemPredicate,
        slots: _TSlots | None = None
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:inventory_changed"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = [item.to_dict() for item in items]
        if slots is not None:
            conditions["slots"] = slots

        return Criteria(
            name = f"inventory_changed_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def item_durability_changed(
        item: ItemPredicate,
        delta: int | Range | None = None,
        durability: int | Range | None = None
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:item_durability_changed"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = item.to_dict()
        if delta is not None:
            if isinstance(delta, int):
                conditions["delta"] = delta
            else:
                conditions["delta"] = {"min": delta.start, "max": delta.end}
        if durability is not None:
            if isinstance(durability, int):
                conditions["durability"] = durability
            else:
                conditions["durability"] = {"min": durability.start, "max": durability.end}
        
        return Criteria(
            name = f"item_durability_changed_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def item_used_on_block(
        *location: Predicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:item_used_on_block"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["location"] = [predicate.to_dict() for predicate in location]

        return Criteria(
            name = f"item_used_on_block_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def location() -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:location"
        data["conditions"] = {}

        return Criteria(
            name = f"location_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def placed_block(
        *location: Predicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:placed_block"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["location"] = [predicate.to_dict() for predicate in location]

        return Criteria(
            name = f"placed_block_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def player_hurt_entity(
        entity: EntityPredicate,
        damage: DamageSourcePredicate,
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:player_hurt_entity"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["entity"] = entity.to_dict()
        conditions["damage"] = damage.to_dict()

        return Criteria(
            name = f"player_hurt_entity_{_c.get()}",
            data = data
        )

    @staticmethod
    def player_interacted_with_entity(
        item: ItemPredicate,
        entity: EntityPredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:player_interacted_with_entity"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["item"] = item.to_dict()
        conditions["entity"] = entity.to_dict()

        return Criteria(
            name = f"player_interacted_with_entity_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def player_killed_entity(
        entity: EntityPredicate,
        killing_blow: DamageSourcePredicate
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:player_killed_entity"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["entity"] = entity.to_dict()
        conditions["killing_blow"] = killing_blow.to_dict()

        return Criteria(
            name = f"player_killed_entity_{_c.get()}",
            data = data
        )

    @staticmethod
    def recipe_crafted(
        recipe_id: Identifier,
        ingredients: Iterable[ItemPredicate] | None = None
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:recipe_crafted"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["recipe"] = str(recipe_id)
        if ingredients is not None:
            conditions["ingredients"] = [ingredient.to_dict() for ingredient in ingredients]

        return Criteria(
            name = f"recipe_crafted_{_c.get()}",
            data = data
        )
    
    @staticmethod
    def recipe_unlocked(
        recipe_id: Identifier
    ) -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:recipe_unlocked"
        data["conditions"] = {}
        conditions = data["conditions"]
        conditions["recipe"] = str(recipe_id)

        return Criteria(
            name = f"recipe_unlocked_{_c.get()}",
            data = data
        )

    @staticmethod
    def slept_in_bed() -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:slept_in_bed"
        data["conditions"] = {}

        return Criteria(
            name = f"slept_in_bed_{_c.get()}",
            data = data
        )

    @staticmethod
    def tick() -> "Criteria":
        data = {}
        data["trigger"] = "minecraft:tick"
        data["conditions"] = {}

        return Criteria(
            name = f"tick_{_c.get()}",
            data = data
        )