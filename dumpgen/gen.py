import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import Callable
from datagen.globals import DatagenConfig
from datagen.utils.minecraft.identifier import Identifier

INPUT_PATH  = DatagenConfig.config["dumperSettings"]["source"]
OUTPUT_PATH = DatagenConfig.config["dumperSettings"]["output"]

INPUT_FILE = Path(INPUT_PATH)
OUTPUT_FILE = Path(OUTPUT_PATH)

def sanitize_constant_name(value: str) -> str:
    sanitized = value.upper()
    for char in ['.', ':', '/', '-', ' ']:
        sanitized = sanitized.replace(char, '_')
    return sanitized.replace("*", "ALL")

def json_list_identifier_str_to_identifier_static_class(json_str: str, class_name: str) -> str:
    dat: list[str] = json.loads(json_str)

    out = "from datagen.utils.minecraft.identifier import Identifier\n\n"
    out += f"class {class_name}():\n"
    for item in dat:
        out += f"    {sanitize_constant_name(item.split(':')[-1])} = Identifier.of('{item}')\n"
    return out

def json_list_str_to_string_static_class(json_str: str, class_name: str) -> str:
    dat: list[str] = json.loads(json_str)

    out = f"class {class_name}():\n"
    for item in dat:
        out += f"    {sanitize_constant_name(item)} = '{item}'\n"
    return out

def json_list_str_to_custom_class_static_class(import_path: str, clazz: str):
    def inner(json_str: str, class_name: str) -> str:
        dat: list[str] = json.loads(json_str)

        out = str()
        if import_path.startswith("from "):
            out += import_path + "\n\n"
        else:
            out += f"from {import_path} import {clazz}\n\n"

        out += f"class {class_name}():\n"
        for item in dat:
            out += f"    {sanitize_constant_name(item)} = {clazz}('{item}')\n"
        return out
    return inner

def json_list_enchantment_data_to_enchantment_static_class(json_str: str, class_name: str) -> str:
    dat: list[dict[str, str]] = json.loads(json_str)

    out = "from datagen.utils.minecraft.identifier import Identifier\n"
    out += "from datagen.utils.repr.enchantment import Enchantment\n\n"
    out += f"class {class_name}():\n"
    for item in dat:
        id = Identifier.of(item["id"])
        out += f"    {sanitize_constant_name(id.get_path())} = Enchantment(Identifier.of('{id}'), {item['max_level']})\n"
    return out
def json_list_identifier_str_to_custom_class_static_class(import_path: str, clazz: str | None = None):
    def inner(json_str: str, class_name: str) -> str:
        dat: list[str] = json.loads(json_str)

        out = str()
        out += "from datagen.utils.minecraft.identifier import Identifier\n"
        if not clazz or import_path.startswith("from "):
            out += import_path + "\n\n"
        else:
            out += f"from {import_path} import {clazz}\n\n"

        out += f"class {class_name}():\n"
        for item in dat:
            out += f"    {sanitize_constant_name(item.split(':')[-1])} = {clazz}(Identifier.of('{item}'))\n"
        return out
    return inner
def main(input: str | Path, output: str | Path, class_name: str, process: Callable[[str, str], str]):
    con = Path(input).read_text()

    out = process(con, class_name)

    Path(output).write_text(out)

def dump_advancement():
    main(
        INPUT_FILE / "advancements.json", 
        OUTPUT_FILE / "advancements.py", 
        "Advancements", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.advancement import Advancement", "Advancement"
        )
    )
def dump_attributes():
    main(
        INPUT_FILE / "attributes.json", 
        OUTPUT_FILE / "attributes.py", 
        "Attributes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.attribute import Attribute", "Attribute"
        )
    )
def dump_biomes():
    main(
        INPUT_FILE / "biomes.json", 
        OUTPUT_FILE / "biomes.py", 
        "Biomes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.biome import Biome", "Biome"
        )
    )
def dump_block_types():
    main(
        INPUT_FILE / "block_types.json", 
        OUTPUT_FILE / "block_types.py", 
        "BlockTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.block_type", "BlockType"
        )
    )
def dump_blocks():
    main(
        INPUT_FILE / "blocks.json", 
        OUTPUT_FILE / "blocks.py", 
        "Blocks", 
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.block", "Block"
        )
    )
def dump_damage_types():
    main(
        INPUT_FILE / "damage_types.json", 
        OUTPUT_FILE / "damage_types.py", 
        "DamageTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.damage import DamageType", "DamageType"
        )
    )
def dump_data_component_types():
    main(
        INPUT_FILE / "data_component_types.json", 
        OUTPUT_FILE / "data_component_types.py", 
        "DataComponentTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.datacomponent import DataComponentType", "DataComponentType"
        )
    )
def dump_dimensions():
    main(
        INPUT_FILE / "dimensions.json",
        OUTPUT_FILE / "dimensions.py",
        "Dimensions",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.dimension", "Dimension"
        )
    )

def dump_dimension_types():
    main(
        INPUT_FILE / "dimension_types.json",
        OUTPUT_FILE / "dimension_types.py",
        "DimensionTypes",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.dimension_type", "DimensionType"
        )
    )

def dump_enchantments_identifiers():
    main(
        INPUT_FILE / "enchantments.json",
        OUTPUT_FILE / "enchantment_identifiers.py",
        "EnchantmentIdentifiers",
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.enchantment import Enchantment", "Enchantment"
        )
    )

def dump_equipment_slots():
    main(
        INPUT_FILE / "equipment_slots.json",
        OUTPUT_FILE / "equipment_slots.py",
        "EquipmentSlots",
        json_list_str_to_custom_class_static_class(
            "from datagen.utils.repr.equipment_slot import EquipmentSlot", "EquipmentSlot"
        )
    )

def dump_fluids():
    main(
        INPUT_FILE / "fluids.json",
        OUTPUT_FILE / "fluids.py",
        "Fluids",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.fluid", "Fluid"
        )
    )

def dump_gamerules():
    main(
        INPUT_FILE / "gamerules.json",
        OUTPUT_FILE / "gamerules.py",
        "Gamerules",
        json_list_str_to_custom_class_static_class(
            "from datagen.utils.repr.gamerule import Gamerule", "Gamerule"
        )
    )

def dump_enchantment_data():
    main(
        INPUT_FILE / "enchantment_data.json", 
        OUTPUT_FILE / "enchantments.py", 
        "Enchantments", 
        json_list_enchantment_data_to_enchantment_static_class
    )
def dump_entity_types():
    main(
        INPUT_FILE / "entity_types.json", 
        OUTPUT_FILE / "entity_types.py", 
        "EntityTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.entitytype", "EntityType"
        )
    )
def dump_instruments():
    main(
        INPUT_FILE / "instruments.json", 
        OUTPUT_FILE / "instruments.py", 
        "Instruments", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.instrument import Instrument", "Instrument"
        )
    )
def dump_items():
    main(
        INPUT_FILE / "items.json", 
        OUTPUT_FILE / "items.py", 
        "Items", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.item import Item", "Item"
        )
    )
def dump_mob_effects():
    main(
        INPUT_FILE / "mob_effects.json",
        OUTPUT_FILE / "mob_effects.py",
        "MobEffects",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.mob_effect", "MobEffect"
        )
    )

def dump_particle_types():
    main(
        INPUT_FILE / "particle_types.json", 
        OUTPUT_FILE / "particle_types.py", 
        "ParticleTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.particle import ParticleType", "ParticleType"
        )
    )
def dump_slot_ranges():
    main(
        INPUT_FILE / "slot_ranges.json",
        OUTPUT_FILE / "slot_ranges.py",
        "SlotRanges",
        json_list_str_to_custom_class_static_class(
            "from datagen.utils.repr.slot_range import SlotRange", "SlotRange"
        )
    )

def dump_status_effects():
    main(
        INPUT_FILE / "status_effects.json",
        OUTPUT_FILE / "status_effects.py",
        "StatusEffects",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.status_effect", "StatusEffect"
        )
    )

def dump_structure_sets():
    main(
        INPUT_FILE / "structure_sets.json",
        OUTPUT_FILE / "structure_sets.py",
        "StructureSets",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.structure_set", "StructureSet"
        )
    )

def dump_structures():
    main(
        INPUT_FILE / "structures.json",
        OUTPUT_FILE / "structures.py",
        "Structures",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.structure", "Structure"
        )
    )

def dump_villager_professions():
    main(
        INPUT_FILE / "villager_professions.json",
        OUTPUT_FILE / "villager_professions.py",
        "VillagerProfessions",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.villager_profession", "VillagerProfession"
        )
    )

def dump_villager_types():
    main(
        INPUT_FILE / "villager_types.json",
        OUTPUT_FILE / "villager_types.py",
        "VillagerTypes",
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.villager_type", "VillagerType"
        )
    )

def dump_sounds():
    main(
        INPUT_FILE / "sounds.json", 
        OUTPUT_FILE / "sounds.py", 
        "Sounds", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.sound import Sound", "Sound"
        )
    )

def dump_all():
    dump_advancement()
    dump_attributes()
    dump_biomes()
    dump_block_types()
    dump_blocks()
    dump_damage_types()
    dump_data_component_types()
    dump_dimensions()
    dump_dimension_types()
    dump_enchantments_identifiers()
    dump_enchantment_data()
    dump_equipment_slots()
    dump_fluids()
    dump_gamerules()
    dump_entity_types()
    dump_instruments()
    dump_items()
    dump_mob_effects()
    dump_particle_types()
    dump_slot_ranges()
    dump_sounds()
    dump_status_effects()
    dump_structure_sets()
    dump_structures()
    dump_villager_professions()
    dump_villager_types()

dump_all()