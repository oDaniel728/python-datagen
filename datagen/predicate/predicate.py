from pathlib import Path
from typing import Any, Literal

from datagen.datapack.namespace import Namespace
from datagen.globals import PREDICATES_PATH
from datagen.predicate.builders import PredicateBuilderUtil
from datagen.utils.json_encoder import dumps
from datagen.utils.obfuscator import Obfuscator
from datagen.types.util.min import Range
from datagen.types.util.validpredicate import ValidPredicate
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.repr.damagesourcepredicate import DamageSourcePredicate
from datagen.utils.repr.enchantedchance import EnchantedChance
from datagen.utils.repr.enchantment import Enchantment
from datagen.utils.repr.entitypredicate import EntityPredicate
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.locationpredicate import LocationPredicate
from datagen.utils.simplefile import SimpleFile

class PredicateType(): pass
class VALUE_CHECK(PredicateType): pass
class RANDOM_CHANCE(PredicateType): pass
class WEATHER_CHECK(PredicateType): pass
class REFERENCE(PredicateType): pass
class ENTITY_SCORES(PredicateType): pass
class INVERTED(PredicateType): pass
class KILLED_BY_PLAYER(PredicateType): pass
class ALL_OF(PredicateType): pass
class ANY_OF(PredicateType): pass
class BLOCK_STATE_PROPERTY(PredicateType): pass
class DAMAGE_SOURCE_PROPERTIES(PredicateType): pass
class ENCHANTMENT_ACTIVE_CHECK(PredicateType): pass
class ENTITY_PROPERTIES(PredicateType): pass
class LOCATION_CHECK(PredicateType): pass
class MATCH_TOOL(PredicateType): pass
class RANDOM_CHANCE_WITH_ENCHANTED_BONUS(PredicateType): pass
class SURVIVES_EXPLOSION(PredicateType): pass
class TABLE_BONUS(PredicateType): pass
class TIME_CHECK(PredicateType): pass

class Predicate[T](ValidPredicate):
    NAMESPACE = Namespace.temp()

    @staticmethod
    def use_namespace(namespace: Namespace):
        Predicate.NAMESPACE = namespace

    __predicates: dict[Identifier, "Predicate"] = {}

    def __new__(cls, id: Identifier, data: dict):
        if id in cls.__predicates:
            instance = cls.__predicates[id]
            instance._data = data
            return instance
        instance = super().__new__(cls)
        cls.__predicates[id] = instance
        return instance

    def __init__(self, id: Identifier, data: dict):
        self._data = data
        self.id = id
        self.namespace = Namespace.temp()
        Predicate.__predicates[id] = self
        self.namespace.add_predicate(self)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Predicate) and self.id == other.id

    def to_dict(self) -> dict:
        return self._data

    def to_string(self) -> str:
        return dumps(self.to_dict(), indent=4)

    def get_filepath(self) -> Path:
        path = Obfuscator.obfuscate_path(self.id.get_namespace(), self.id.get_path(), "identifiers.predicates")
        return Path(PREDICATES_PATH) / (path.replace(".", "/").lower() + ".json")

    def to_file(self) -> SimpleFile:
        return SimpleFile(self.get_filepath(), self.to_string())

    @staticmethod
    def value_check(
        value: str, 
        range: Range
    ) -> "Predicate[VALUE_CHECK]":
        return Predicate(Predicate.NAMESPACE / f"valchk_{value}_{range.start}_{range.end}", {
            "condition": "minecraft:value_check",
            "value": value,
            "range": {
                "min": range.start,
                "max": range.end
            }
        })
    
    @staticmethod
    def random_chance(
        chance: float
    ) -> "Predicate[RANDOM_CHANCE]":
        return Predicate(Predicate.NAMESPACE / f"random_{str(chance).replace('.', '_')}", {
            "condition": "minecraft:random_chance",
            "chance": chance
        })
    
    @staticmethod
    def weather_check(
        raining: bool, 
        thundering: bool
    ) -> "Predicate[WEATHER_CHECK]":
        return Predicate(Predicate.NAMESPACE / f"wthchk_r{raining}_t{thundering}", {
            "condition": "minecraft:weather_check",
            "raining": raining,
            "thundering": thundering
        })
    
    @staticmethod
    def reference(
        id: "Identifier | Predicate"
    ) -> "Predicate[REFERENCE]":
        if isinstance(id, Predicate):
            id = id.id
        return Predicate(Predicate.NAMESPACE / f"ref_{id.get_namespace()}_{id.get_path()}", {
            "condition": "minecraft:reference",
            "name": str(id)
        })
    
    _TEntityContext = Literal["this", "attacker", "direct_attacker", "attacking_player"]
    @staticmethod
    def entity_scores(
        entity: _TEntityContext, 
        scores: dict[str, Range]
    ) -> "Predicate[ENTITY_SCORES]":
        return Predicate(Predicate.NAMESPACE / f"scores_{entity}_{'_'.join([f'{k}_{v.start}_{v.end}' for k, v in scores.items()])}", {
            "condition": "minecraft:entity_scores",
            "entity": entity,
            "scores": {k: {"min": v.start, "max": v.end} for k, v in scores.items()}
        })
    
    @staticmethod
    def inverted(
        predicate: "Predicate"
    ) -> "Predicate[INVERTED]":
        return Predicate(Predicate.NAMESPACE / f"inv_{predicate.id.get_namespace()}_{predicate.id.get_path()}", {
            "condition": "minecraft:inverted",
            "predicate": predicate._data
        })

    @staticmethod
    def killed_by_player() -> "Predicate[KILLED_BY_PLAYER]":
        return Predicate(Predicate.NAMESPACE / "klld_by_plr", {
            "condition": "minecraft:killed_by_player"
        })

    @staticmethod
    def all_of(
        *predicates: "Predicate"
    ) -> "Predicate[ALL_OF]":
        return Predicate(Predicate.NAMESPACE / f"allof_{'_'.join([p.id.get_namespace() + '_' + p.id.get_path() for p in predicates])}", {
            "condition": "minecraft:all_of",
            "terms": [p._data for p in predicates]
        })
    
    @staticmethod
    def any_of(
        *predicates: "Predicate"
    ) -> "Predicate[ANY_OF]":
        return Predicate(Predicate.NAMESPACE / f"anyof_{'_'.join([p.id.get_namespace() + '_' + p.id.get_path() for p in predicates])}", {
            "condition": "minecraft:any_of",
            "terms": [p._data for p in predicates]
        })
    
    @staticmethod
    def block_state_property(
        block: Block, 
        properties: dict[str, Any]
    ) -> "Predicate[BLOCK_STATE_PROPERTY]":
        return Predicate(Predicate.NAMESPACE / f"bsp_{block.id.get_namespace()}_{block.id.get_path()}_{'_'.join([f'{k}_{v}' for k, v in properties.items()])}", {
            "condition": "minecraft:block_state_property",
            "block": str(block),
            "properties": properties
        })

    @staticmethod
    def damage_source_properties(
        predicate: DamageSourcePredicate
    ) -> "Predicate[DAMAGE_SOURCE_PROPERTIES]":
        predicate_data = PredicateBuilderUtil.to_dict(predicate)
        return Predicate(Predicate.NAMESPACE / f"dsp_{PredicateBuilderUtil.id_suffix(predicate_data)}", {
            "condition": "minecraft:damage_source_properties",
            "predicate": predicate_data
        })

    @staticmethod
    def enchantment_active_check(
        active: bool = True
    ) -> "Predicate[ENCHANTMENT_ACTIVE_CHECK]":
        data: dict[str, Any] = {
            "condition": "minecraft:enchantment_active_check"
        }
        if not active:
            data["active"] = False
        return Predicate(Predicate.NAMESPACE / f"eac_{active}", data)

    @staticmethod
    def entity_properties(
        entity: _TEntityContext, 
        predicate: EntityPredicate
    ) -> "Predicate[ENTITY_PROPERTIES]":
        predicate_data = PredicateBuilderUtil.to_dict(predicate)
        return Predicate(Predicate.NAMESPACE / f"eprop_{PredicateBuilderUtil.id_suffix(entity, predicate_data)}", {
            "condition": "minecraft:entity_properties",
            "entity": entity,
            "predicate": predicate_data
        })

    @staticmethod
    def location_check(
        predicate: LocationPredicate, 
        offset_x: int = 0, 
        offset_y: int = 0, 
        offset_z: int = 0
    ) -> "Predicate[LOCATION_CHECK]":
        predicate_data = PredicateBuilderUtil.to_dict(predicate)
        data: dict[str, Any] = {
            "condition": "minecraft:location_check",
            "predicate": predicate_data
        }
        if offset_x != 0:
            data["offsetX"] = offset_x
        if offset_y != 0:
            data["offsetY"] = offset_y
        if offset_z != 0:
            data["offsetZ"] = offset_z

        return Predicate(Predicate.NAMESPACE / f"locchk_{PredicateBuilderUtil.id_suffix(offset_x, offset_y, offset_z, predicate_data)}", data)

    @staticmethod
    def match_tool(
        predicate: ItemPredicate
    ) -> "Predicate[MATCH_TOOL]":
        predicate_data = PredicateBuilderUtil.to_dict(predicate)
        return Predicate(Predicate.NAMESPACE / f"tool_{PredicateBuilderUtil.id_suffix(predicate_data)}", {
            "condition": "minecraft:match_tool",
            "predicate": predicate_data
        })

    @staticmethod
    def random_chance_with_enchanted_bonus(
        unenchanted_chance: float, 
        enchanted_chance: EnchantedChance, 
        enchantment: Enchantment
    ) -> "Predicate[RANDOM_CHANCE_WITH_ENCHANTED_BONUS]":
        enchanted_chance_data = PredicateBuilderUtil.to_dict(enchanted_chance)
        return Predicate(Predicate.NAMESPACE / f"rcweb_{PredicateBuilderUtil.id_suffix(unenchanted_chance, enchantment, enchanted_chance_data)}", {
            "condition": "minecraft:random_chance_with_enchanted_bonus",
            "unenchanted_chance": unenchanted_chance,
            "enchanted_chance": enchanted_chance_data,
            "enchantment": str(enchantment)
        })

    @staticmethod
    def survives_explosion() -> "Predicate[SURVIVES_EXPLOSION]":
        return Predicate(Predicate.NAMESPACE / "survexplosion", {
            "condition": "minecraft:survives_explosion"
        })

    @staticmethod
    def table_bonus(
        enchantment: Enchantment, 
        chances: list[float]
    ) -> "Predicate[TABLE_BONUS]":
        return Predicate(Predicate.NAMESPACE / f"tabbonus_{PredicateBuilderUtil.id_suffix(enchantment, *chances)}", {
            "condition": "minecraft:table_bonus",
            "enchantment": str(enchantment),
            "chances": chances
        })

    @staticmethod
    def time_check(
        value: Range, 
        period: int | None = None
    ) -> "Predicate[TIME_CHECK]":
        data = {
            "condition": "minecraft:time_check",
            "value": {
                "min": value.start,
                "max": value.end
            }
        }
        if period is not None:
            data["period"] = period

        return Predicate(Predicate.NAMESPACE / f"tmchk_{PredicateBuilderUtil.id_suffix(value.start, value.end, period)}", data)
