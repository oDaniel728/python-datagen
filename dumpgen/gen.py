import json
from pathlib import Path
from typing import Callable

import sys
sys.path.append(str(Path(__file__).parent.parent))
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.repr.enchantment import Enchantment
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.instrument import Instrument

INPUT_PATH  = "dumpgen/dumps/block_types.json"
CLASS_NAME  = "BlockTypes"
OUTPUT_PATH = "dumpgen/dumps/block_types.py"

INPUT_FILE = Path(INPUT_PATH)
OUTPUT_FILE = Path(OUTPUT_PATH)

def json_list_identifier_str_to_identifier_static_class(json_str: str, class_name: str) -> str:
    dat: list[str] = json.loads(json_str)

    out = str()
    out += "from datagen.utils.minecraft.identifier import Identifier\n\n"
    out += f"class {class_name}():\n"
    for item in dat:
        out += f"    {item.split(':')[-1].upper()} = Identifier.of('{item}')\n"
    return out
def json_list_enchantment_data_to_enchantment_static_class(json_str: str, class_name: str) -> str:
    dat: list[dict[str, str]] = json.loads(json_str)

    out = str()
    out += "from datagen.utils.minecraft.identifier import Identifier\n"
    out += "from datagen.utils.repr.enchantment import Enchantment\n"
    out += "\n"
    out += f"class {class_name}():\n"
    for item in dat:
        id = Identifier.of(item["id"])
        out += f"    {id.get_path().upper()} = Enchantment(Identifier.of('{id}'), {item['max_level']})\n"
    return out
def json_list_identifier_str_to_custom_class_static_class(import_path: str, clazz: str | None = None):
    def inner(json_str: str, class_name: str) -> str:
        dat: list[str] = json.loads(json_str)

        out = str()
        out += "from datagen.utils.minecraft.identifier import Identifier\n"
        if not clazz or import_path.startswith("from "):
            out += import_path + "\n\n"
        else: out += f"from {import_path} import {clazz}\n\n"

        out += f"class {class_name}():\n"
        for item in dat:
            out += f"    {item.split(':')[-1].upper().replace('.', '_')} = {clazz}(Identifier.of('{item}'))\n"
        return out
    return inner
def main(input: str | Path, output: str | Path, class_name: str, process: Callable[[str, str], str]):
    con = Path(input).read_text()

    out = process(con, class_name)

    Path(output).write_text(out)

def dump_block_types():
    main(
        "dumpgen/dumps/block_types.json", 
        "dumpgen/dumps/block_types.py", 
        "BlockTypes", 
        json_list_identifier_str_to_identifier_static_class
    )
def dump_blocks():
    main(
        "dumpgen/dumps/blocks.json", 
        "dumpgen/dumps/blocks.py", 
        "Blocks", 
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.block", "Block"
        )
    )
def dump_enchantment_data():
    main(
        "dumpgen/dumps/enchantment_data.json", 
        "dumpgen/dumps/enchantments.py", 
        "Enchantments", 
        json_list_enchantment_data_to_enchantment_static_class
    )
def dump_entity_types():
    main(
        "dumpgen/dumps/entity_types.json", 
        "dumpgen/dumps/entity_types.py", 
        "EntityTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "datagen.utils.repr.entitytype", "EntityType"
        )
    )
def dump_instruments():
    main(
        "dumpgen/dumps/instruments.json", 
        "dumpgen/dumps/instruments.py", 
        "Instruments", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.instrument import Instrument", "Instrument"
        )
    )

def dump_items():
    main(
        "dumpgen/dumps/items.json", 
        "dumpgen/dumps/items.py", 
        "Items", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.item import Item", "Item"
        )
    )

def dump_particle_types():
    main(
        "dumpgen/dumps/particle_types.json", 
        "dumpgen/dumps/particle_types.py", 
        "ParticleTypes", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.particle import ParticleType", "ParticleType"
        )
    )

def dump_sounds():
    main(
        "dumpgen/dumps/sounds.json", 
        "dumpgen/dumps/sounds.py", 
        "Sounds", 
        json_list_identifier_str_to_custom_class_static_class(
            "from datagen.utils.repr.sound import Sound", "Sound"
        )
    )

def dump_all():
    dump_block_types()
    dump_blocks()
    dump_enchantment_data()
    dump_entity_types()
    dump_instruments()
    dump_items()
    dump_particle_types()
    dump_sounds()

dump_all()