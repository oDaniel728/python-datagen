# Skill: python-datagen

# python-datagen — Minecraft Java Edition Datapack Generator (1.21+)

## Visão Geral

python-datagen é uma **biblioteca Python** que gera **datapacks para Minecraft Java Edition 1.21+** programaticamente. Você escreve código Python que descreve functions, loot tables, advancements, recipes, tags, predicates, etc., e a biblioteca gera a estrutura completa de pastas e arquivos JSON/MCfunction.

---

## Estrutura do Projeto

```
python-datagen/
  __main__.py           # Entry point: `python .` ou `python . -w` (watch mode)
  .datagenconfig        # Config JSON (source, output, obfuscation, logging)
  datagen/              # Core library (library de geração)
    __init__.py          # Empty
    globals.py           # Path constants + DatagenConfig singleton
    advancement/     # Mobs, items, etc.
    function/            # Funções e comandos
      function.py        # .mcfunction files
      commands/          # ~57 comandos vanilla (say, give, execute, etc.)
    loot_table/          # Loot tables completas
    predicate/           # Predicates (experimental)
    recipes/             # Crafting recipes
    tag/                 # Tags (item, block, function, enchantment)
    types/               # Type system (text components, protocols, structs)
    utils/               # Utilities (Identifier, TargetSelector, Logger, etc.)
    utils/repr/          # ~47 value objects (Item, Block, ItemStack, etc.)
    utils/minecraft/collections/  # Auto-generated constants (Items, Blocks, etc.)
  datagenpp/             # Datagen++ (extensões de alto nível)
    extras/
      packs/pack.py      # Classe base Pack com lifecycle hooks
      scripts/           # Script/ScriptBuilder
      itempack.py        # ItemPack (batch give/summon/bundle)
      item/              # Entity spawn eggs, command blocks
      recipes/           # Recipe utilities
      repr/              # Entity representations
  src/                   # SEU código — packs do usuário
    main.py              # Entry point do usuário (chamado por __main__.py)
    packs/               # Seus packs aqui
  dumpgen/               # DumpGen tool (regenerates constant classes)
  docs/                  # Documentação markdown (14 páginas)
  datapacks/             # OUTPUT — datapacks gerados aqui
```

---

## Como Executar

```bash
# Uma vez (gera tudo e termina)
python .

# Watch mode (hot-reload ao alterar src/)
python . -w
# ou
python . --watch
```

O entry point `__main__.py` adiciona `src/` ao `sys.path`, importa `src.main` e chama `main()`.

---

## Ciclo de Vida de um Pack

```python
from datagenpp.extras.packs.pack import Pack

class MeuPack(Pack, name='meupack', description='Descrição'):
    def on_prepare(self) -> None:
        # Setup inicial (criar variáveis, configs)
        pass

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        # Registrar functions, tags, loot tables, etc.
        # ns = namespace do pack (ex: 'meupack')
        # mc = namespace 'minecraft' (para load/tick tags)
        # tmp = namespace 'temp' (para temporários)
        pass

    def on_build(self) -> None:
        # Pós-build (se precisar)
        pass
```

**Importante:** `name` é o nome do diretório do datapack E do namespace principal. Passado como kwarg na `__init_subclass__`.

### Lifecycle internos (Pack.__init__)

1. `__prepare__()`: cria `ns`, `mc`, `tmp` Namespaces, chama `on_prepare()`
2. `__register__()`: registra namespaces no `DataPack`, chama `on_register(ns, mc, tmp)`
3. `__build__()`: chama `dp.build()`, chama `on_build()`

---

## Convenções de Código

### Geral (ver também python-dev-gen skill)

- **Python 3.12+** com type hints modernos (genéricos `[T]`, `|`, etc.)
- **Classes SEMPRE com parênteses**: `class Foo():`, `class Bar(Base):`
- **Docstrings em TUDO** (classes, métodos, funções) com `Examples:` em doctest
- **Atributos privados** com `__` (name mangling), getters/setters estilo Java
- **Atributos protegidos** com `_` (subclasses)
- **Classes estáticas** para namespaces organizados (`@staticmethod` e `@classmethod`)
- **Sempre POO** — nada de funções soltas fora de classes
- **NUNCA comentários** (`#`) no código — apenas docstrings
- `# type: ignore` permitido para falsos positivos de mypy

### Imports

```python
# Imports absolutos de datagen.*
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.function.commands.execute import Execute
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
```

---

## API Patterns Essenciais

### 1. Namespace

Namespace agrupa recursos de um datapack. É um `Identifier` com açúcar:

```python
ns = Namespace("meupack")        # Cria ns meupack
mc = Namespace.minecraft()       # Namespace 'minecraft'
tmp = Namespace.temp()           # Namespace 'temp' (para temporários)

# Namespace + caminho = Identifier
ns / "path/to/file"    # => Identifier("meupack:path/to/file")
mc / "tags/function/load.json"  # => Identifier("minecraft:tags/function/load.json")
```

### 2. Function (.mcfunction)

```python
with Function(ns / "caminho/nome") as func:
    ~ Say("Hello!")
    ~ Give(TargetSelector.SELF, Items.DIAMOND)
    # Comandos são adicionados com ~ (operador invert)

ns += func              # Registra a function no namespace
mc.load += func         # Adiciona à tag minecraft:load
mc.tick += func         # Adiciona à tag minecraft:tick
```

### 3. Comandos

Todos os comandos estão em `datagen/function/commands/`. Use `~` (operador `__invert__`) para marcar um comando para execução:

```python
~ Say("texto")
~ Give(TargetSelector.SELF, Items.DIAMOND)
~ Execute().AS(TargetSelector.ALL_PLAYERS).RUN(comando)
~ Scoreboard.players_set(TargetSelector.SELF, SCORE, 10)
~ Clear(TargetSelector.ALL_PLAYERS, Items.BUNDLE)
```

### 4. TargetSelector

```python
TargetSelector.SELF                       # @s
TargetSelector.ALL_PLAYERS                # @a
TargetSelector.ALL_ENTITIES               # @e
TargetSelector.NEAREST_PLAYER             # @p
TargetSelector.RANDOM_PLAYER              # @r

# Com filtros:
TargetSelector.ALL_ENTITIES.with_settings(
    TargetSelectorSettings()
    .with_tag("mytag")
    .with_type(EntityTypes.ZOMBIE)
    .with_distance((0, 10))
)
```

### 5. Data Storage

```python
from datagen.function.commands._data.datastorage import DataStorage

store = DataStorage(ns / "my_data")
~ store["path"]["to"]["value"].set(42)
~ store["name"].set('{"text":"Hello"}')
```

### 6. EntityData / BlockEntityData (1.21+)

```python
from datagen.function.commands._data.entitydata import EntityData

entity = EntityData(TargetSelector.SELF)
~ entity["Health"].set(20)
~ entity["CustomName"].set('{"text":"Boss"}')
~ entity["Inventory"][0]["Slot"].set(0)
```

**Como argumento de função:** EntityData pode ser passado como argumento para `Function.run()` — ele copia os dados para storage temp, chama a função, e descarta:

```python
with AnonymousFunction() as fn:
    # usa args["Health"] no temp storage
    tmp += fn

args = DataStorage(tmp / "args")
~ args["Health"].set(entity["Health"])
~ fn.run(args)
```

### 7. AnonymousFunction

Functions auto-geradas com nomes únicos (`fun0`, `fun1`, ...):

```python
from datagen.function.anonymousfunction import AnonymousFunction

with AnonymousFunction() as fn:
    ~ Say("auto-generated!")
    tmp += fn  # registra no namespace temp
```

### 8. Item e ItemStack

```python
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.minecraft.collections.items import Items

# Item simples
item = Item(Identifier.of("minecraft:diamond"))

# Item com settings customizados
class MeuItemSettings(Item.Settings):
    def get_components(self) -> dict:
        return {"minecraft:custom_name": '{"text":"Especial"}'}

class MeuItem(Item[MeuItemSettings]):
    def __init__(self) -> None:
        super().__init__(Identifier.of("minecraft:stick"), MeuItemSettings())

# ItemStack (item + count + NBT)
stack = ItemStack(item, count=3)
stack = item.get_stack(10)  # shorthand

# Constantes pré-definidas (auto-geradas)
Items.DIAMOND
Items.STICK
Items.BUNDLE
```

---

## Loot Table System (1.21+)

Sistema de loot tables completo com builder fluente.

### Exemplo Básico

```python
from datagen.loot_table.loot_table import LootTable, LootConditions, LootFunctions

loot = (LootTable.builder(ns / "tables/minha_tabela")
    .pool(1)  # rolls: int, tuple, ou dict
        .entry("minecraft:item", Items.DIAMOND).weight(1).then()
        .entry("minecraft:item", Items.EMERALD).weight(2)
            .function(lambda f: f.set_count((1, 3)))
        .then()
    .end_pool()
    .pool((2, 4))
        .condition(lambda c: c.random_chance(0.5))
        .entry("minecraft:item", "minecraft:iron_ingot").weight(3).then()
        .entry("minecraft:empty").weight(1).then()
    .end_pool()
.seal())

ns += loot  # Registra no namespace, gera o JSON
```

### Tipos de Entry

| Método | Tipo | Campo ID |
|--------|------|----------|
| `.entry("minecraft:item", id)` | Item único | `name` |
| `.entry("minecraft:loot_table", id)` | Referência a outra loot table | `value` (1.21+) |
| `.tag(tag_id)` | Tag de itens (com `expand`) | `name` |
| `.dynamic(name)` | Drop dinâmico (contents, sherds) | `name` |
| `.group()` | Grupo de entries (compósito) | children[] |
| `.alternatives()` | Primeiro entry que passar | children[] |
| `.sequence()` | Sequência até falhar | children[] |
| `.entry("minecraft:empty") | Nada | — |

### Entry Compósito (group/alternatives/sequence)

```python
.pool(1)
    .group()
        .child("minecraft:item", "minecraft:apple")
        .child("minecraft:item", "minecraft:golden_apple")
    .then()
.end_pool()
```

### Entry Tag

```python
.tag("#minecraft:arrows", expand=True).weight(1).then()
```

### Entry LootTable com value

```python
# Auto-detects loot_table type → usa "value" em vez de "name"
.entry("minecraft:loot_table", "minecraft:chests/simple_dungeon")

# Ou explicitamente com .value()
.entry("minecraft:loot_table").value(Identifier.of("minecraft:chests/simple_dungeon"))
```

### Context Type (1.21+)

```python
(LootTable.builder(ns / "entities/zombie")
    .context_type("minecraft:entity")
    ...
)
```

Tipos: `minecraft:generic` (default), `minecraft:entity`, `minecraft:block`, `minecraft:chest`, `minecraft:fishing`, `minecraft:equipment`, `minecraft:empty`, `minecraft:gift`, `minecraft:advancement_reward`, `minecraft:advancement_entity`, `minecraft:barter`, `minecraft:archaeology`

### Random Sequence (seed determinística)

```python
(LootTable.builder(ns / "tables/seedada")
    .random_sequence("mypack:sequencia_unica")
    ...
)
```

### Condições (LootConditions)

Todas as condições 1.21+:

```python
lambda c: c.random_chance(0.5)
lambda c: c.random_chance(0.5)                         # float ou number provider dict
lambda c: c.random_chance({"min": 0.1, "max": 0.5})     # number provider (1.21+)
lambda c: c.random_chance_with_enchanted_bonus(enchantment, unenchanted_chance=0.1, enchanted_chance=LevelBasedValue.linear(0.19, 0.09))
lambda c: c.killed_by_player()
lambda c: c.entity_properties("this", predicate_dict)
lambda c: c.entity_scores("this", {"objective": {"min": 5}})
lambda c: c.location_check(predicate_dict, offset_x=0, offset_y=0, offset_z=0)
lambda c: c.weather_check(raining=True)
lambda c: c.table_bonus(enchantment, [0.1, 0.2, 0.3, 0.4])
lambda c: c.time_check(6000)
lambda c: c.damage_source_properties(predicate_dict)
lambda c: c.match_tool(predicate_dict)
lambda c: c.reference("mypack:my_predicate")
lambda c: c.survives_explosion()
lambda c: c.inverted(other_condition)
lambda c: c.any_of(cond1, cond2)
lambda c: c.all_of(cond1, cond2)
lambda c: c.block_state_property("minecraft:chest", {"facing": "north"})
lambda c: c.value_check(value, {"min": 1, "max": 10})
lambda c: c.enchantment_active_check(True)   # Novo em 1.21
```

### Funções (LootFunctions)

```python
lambda f: f.set_count((1, 3))
lambda f: f.set_damage(0.5)
lambda f: f.enchant_randomly()
lambda f: f.enchant_randomly(["minecraft:sharpness", "minecraft:unbreaking"])
lambda f: f.enchant_with_levels(30)
lambda f: f.set_components({"minecraft:custom_name": '{"text":"Sword"}'})  # 1.21+
lambda f: f.set_name('{"text":"Special"}')
lambda f: f.set_lore(['{"text":"Legendary"}'])
lambda f: f.furnace_smelt()
lambda f: f.set_potion("minecraft:healing")
lambda f: f.set_ominous_bottle(3)
lambda f: f.explosion_decay()
lambda f: f.copy_state("minecraft:chest", ["facing"])
```

### LevelBasedValue (1.21+)

```python
from datagen.utils.repr.levelbasedvalue import LevelBasedValue

LevelBasedValue.constant(0.5)                                              # { "type": "constant", "value": 0.5 }
LevelBasedValue.linear(0.1, 0.09)                                          # { "type": "linear", "base": 0.1, "per_level_above_first": 0.09 }
LevelBasedValue.levels_squared(1.5)                                        # { "type": "levels_squared", "added": 1.5 }
LevelBasedValue.clamped(LevelBasedValue.linear(0.1, 0.09), 0.0, 1.0)      # { "type": "clamped", ... }
LevelBasedValue.fraction(numerator, denominator)                           # { "type": "fraction", ... }
LevelBasedValue.lookup([0.1, 0.2, 0.3], [0.5, 0.6])                       # { "type": "lookup", ... }
```

---

## Custom Enchantments (1.21+)

Enchantments use the `EnchantmentProvider` class. Built via `ns += enchantment` (NOT `~enchantment`, since `Namespace.temp()` is not a singleton).

### Required fields

| Field | Method | Description |
|---|---|---|
| `description` | `.with_description(TextComponent)` | Display name |
| `max_level` | `.with_max_level(int)` | 1–255 |
| `supported_items` | `.with_supported_items(str)` | Items the enchantment applies to (item ID or `#`tag). **Required for `/enchant` and anvil** |
| `primary_items` | `.with_primary_items(str)` | (Optional subset) Controls enchanting table availability |
| `weight` | `.with_weight(int)` | 1–1024. Higher = more common in enchanting table |
| `min_cost`, `max_cost` | `.with_cost(min_base, min_per_level, max_base, max_per_level)` | Enchanting cost formula |
| `anvil_cost` | `.with_anvil_cost(int)` | Base anvil cost |
| `slots` | `.with_slots(str)`, `.with_slots(list)` | Which equipment slots activate effects (`"hand"`, `"armor"`, `"any"`) |
| `effects` | `.with_effects(dict)` | Enchantment effects (value, entity, location, attribute) |

### Minimal `/enchant`-compatible example

```python
enchant = EnchantmentProvider(ns / "my_enchant")
enchant \
    .with_description(LiteralText("My Enchant")) \
    .with_max_level(3) \
    .with_supported_items("#minecraft:enchantable/durability") \
    .with_primary_items("#minecraft:enchantable/durability") \
    .with_weight(5) \
    .with_cost(1, 10, 15, 10) \
    .with_anvil_cost(3) \
    .with_slots("hand")
ns += enchant
```

### JSON output location
`data/<namespace>/enchantment/<id>.json`

---

## Tags

```python
from datagen.tag.itemtag import ItemTag
from datagen.tag.functiontag import FunctionTag

# Tags de função (load/tick) já vêm prontas em mc.load / mc.tick
mc.load += minha_function

# Tags de item personalizadas
itens_tag = ItemTag(ns / "minhas_coisas")
itens_tag.add(Items.DIAMOND)
itens_tag.add(Items.EMERALD)
ns += itens_tag
```

---

## Recipes

```python
from datagen.recipes.recipe import Recipe

recipe = Recipe.builder(ns / "diamond_from_sticks") \
    .pattern("aa", "aa") \
    .key("a", Items.STICK) \
    .result(Items.DIAMOND) \
    .seal()

ns += recipe
```

---

## Text Components (tellraw, títulos, books)

```python
from datagen.utils.minecraft.text._components import LiteralText, ScoreText, TranslatableText

Texto = LiteralText("Hello", color="gold", bold=True)
Score = ScoreText("player", "objective")
Texto = TranslatableText("block.minecraft.diamond_block")

# Uso em comandos:
~ Tellraw(TargetSelector.ALL_PLAYERS, Texto)
~ Title(TargetSelector.ALL_PLAYERS).title(Texto)
```

---

## Scoreboard

```python
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagen.utils.scoreboard.criterion import ObjectiveCriterion

SCORE = ~ Scoreboard.objective("my_obj", LiteralText.EMPTY, ObjectiveCriterion.DUMMY)

# Manipular scores
~ SCORE.player(TargetSelector.SELF).set(10)
~ SCORE.player("@a").add(1)
~ SCORE.player("@r").remove(5)

# Verificar no execute
~ Execute().IF().score(SCORE.player("@s"), matches=(5, 10)).RUN(...)
```

---

## Constants Auto-Geradas

`datagen/utils/minecraft/collections/` contém **34 arquivos** com constantes para tudo no Minecraft:

```python
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.enchantments import Enchantments
from datagen.utils.minecraft.collections.sounds import Sounds
from datagen.utils.minecraft.collections.biomes import Biomes
from datagen.utils.minecraft.collections.gamerules import Gamerules
from datagen.utils.minecraft.collections.attributes import Attributes
from datagen.utils.minecraft.collections.mob_effects import MobEffects
from datagen.utils.minecraft.collections.status_effects import StatusEffects

Items.DIAMOND          # => Identifier("minecraft:diamond")
Items.STICK            # => Identifier("minecraft:stick")
Blocks.STONE           # => Identifier("minecraft:stone")
EntityTypes.ZOMBIE     # => Identifier("minecraft:zombie")
Enchantments.SHARPNESS # => Enchantment(id, max_level)
Enchantments.LOOTING   # => Enchantment(id, max_level)
```

---

## Output

O build gera em `datapacks/<pack_name>/`:

```
datapacks/csys/
  pack.mcmeta                    # pack metadata
  data/csys/
    function/*.mcfunction         # Funções
    loot_table/**/*.json          # Loot tables
    tags/**/*.json                # Tags
    recipes/**/*.json             # Receitas
  data/minecraft/
    tags/function/load.json       # load tag
    tags/function/tick.json       # tick tag
  data/temp/
    function/fun0.mcfunction      # AnonymousFunctions
```

---

## Linguagem Padrão

- **Português** para comunicação com o usuário (mensagens, docstrings, nomes de packs)
- **Inglês** para código/comentários técnicos (identificadores Minecraft, nomes de métodos)

---

## DumpGen (Regenerar Constantes)

```bash
# Se você atualizar os dumps do Minecraft:
python dumpgen/gen.py
```

Lê de `dumpgen/dumps/`, escreve em `datagen/utils/minecraft/collections/`.

---

## Config (.datagenconfig)

O config fica na raiz do projeto e define output, indent, obfuscation e **pack_format**.

```json
{
    "builderSettings": {
        "output": "datapacks/",
        "indent": 4,
        "obfuscate": false,
        "pack_format": 41
    }
}
```

| Pack Format | Minecraft Version |
|---|---|
| 41 | 1.21–1.21.1 |
| 46 | 1.21.2–1.21.3 |
| 47 | 1.21.4 |
| 48 | 1.21.5 |

> **Atenção:** `supported_items` em 1.21–1.21.1 só aceita IDs literais (`"minecraft:stick"`), **não** tags com `#`. Tags passaram a ser suportadas no 1.21.2 (24w33a).

### ⚠️ Dynamic Registries — Precisa Reiniciar o Mundo

Encantamentos, pinturas, instrumentos, e outros recursos marcados com `*` na [wiki de Data Pack](https://minecraft.wiki/w/Data_Pack#Folder_structure) usam **dynamic registries** (experimental settings).

Isso significa que **`/reload` NÃO é suficiente** — você precisa **fechar e reabrir o mundo** (ou reiniciar o servidor) para as mudanças fazerem efeito.

> "Internally, most experimental settings use dynamic registries. This means any changes regarding these features cannot be loaded using the `/reload` command: the world must be exited and reopened."

**Fluxo correto:**
1. `python3 __main__.py` — gera o datapack
2. Copia a pasta `datapacks/csys/` pro mundo
3. **Fecha o mundo completamente** (volta ao menu)
4. **Reabre o mundo**
5. `/enchant @p csys:bundles` — agora funciona

```json
{
    "builderSettings": {
        "source": "src/",
        "output": "datapacks/",
        "comment": false,
        "allowEmptyLines": false,
        "obfuscate": false,
        "indent": 4
    },
    "dumperSettings": { ... },
    "loggerSettings": { ... },
    "environmentSettings": { ... }
}
```

- `obfuscate`: se true, ofusca caminhos de functions/loot tables
- `comment`: adiciona comentários nos arquivos gerados
- `output`: diretório de saída dos datapacks

---

## Comandos para Lint/Type Check

```bash
ruff check datagen/ datagenpp/ src/
mypy datagen/ datagenpp/ src/ --check-untyped-defs
```

Os comandos rodam da raiz do projeto.

---

## Convenções de Arquitetura

### DataStorage vs EntityData vs BlockEntityData

| Classe | Comando MC | Uso |
|--------|-----------|-----|
| `DataStorage` | `/data storage` | Dados persistentes por storage |
| `EntityData` | `/data entity` | Dados de entidades vivas |
| `BlockEntityData` | `/data block` | Dados de block entities |

**Cross-compatible:** Todos os três implementam `set()`, `set_into()`, `to_data()`, `from_data()`, `__lshift__()` e podem ser usados como argumentos de `Function.run()`.

### Identifier (Namespace:Path)

```python
Identifier.of("minecraft:diamond")
Identifier.of("namespace", "path/to/file")
ns / "path"             # Namespace + caminho
```

### ToDict Protocol

Objetos que podem ser convertidos para dicionário implementam `ToDict` com método `to_dict()`. Usado extensivamente para serialização JSON.

### Loot Table Root Type

Em 1.21+, o `type` no root da loot table é o **context type** (ex: `minecraft:entity`, `minecraft:chest`, `minecraft:generic`). O builder usa `minecraft:generic` como padrão.
