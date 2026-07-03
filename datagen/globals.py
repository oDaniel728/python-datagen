import json
from typing import TypedDict


FUNCTIONS_PATH = "function/"
TAGS_PATH = "tags/"
PREDICATES_PATH = "predicate/"
RECIPES_PATH = "recipe/"
ADVANCEMENTS_PATH = "advancement/"
LOOT_TABLES_PATH = "loot_table/"
CONFIG_PATH = "datagen.json"

class DatagenConfig():
    class TDatagenConfigTObfuscationIdentifiers(TypedDict):
        functions: bool
        tags: bool
        advancements: bool
        predicates: bool
        loot_tables: bool
        data_storages: bool

    class TDatagenConfigTObfuscationOtherScoreboard(TypedDict):
        objectives: bool
        players: bool

    class TDatagenConfigTObfuscationOther(TypedDict):
        scoreboard: DatagenConfig.TDatagenConfigTObfuscationOtherScoreboard
        entity_teams: bool
        entity_tags: bool
        item_custom_data_keys: bool

    class TDatagenConfigTObfuscationWhere(TypedDict):
        identifiers: DatagenConfig.TDatagenConfigTObfuscationIdentifiers
        other: DatagenConfig.TDatagenConfigTObfuscationOther

    class TDatagenConfigTObfuscation(TypedDict):
        enabled: bool
        where: DatagenConfig.TDatagenConfigTObfuscationWhere

    class TDatagenConfigTBuilderOptions(TypedDict):
        source: str
        output: str
        indent: int
        comment: bool
        allowEmptyLines: bool
        obfuscation: DatagenConfig.TDatagenConfigTObfuscation
        pack_format: int
    class TDataGenConfigTDumperSettings(TypedDict):
        source: str
        output: str

    class TDatagenConfigTLoggerLevels(TypedDict):
        debug: bool
        success: bool
        info: bool
        warning: bool
        error: bool
        task: bool

    class TDatagenConfigTLoggerWhitelist(TypedDict):
        enabled: bool
        values: list[str]

    class TDatagenConfigTLoggerSettings(TypedDict):
        enabled: bool
        levels: DatagenConfig.TDatagenConfigTLoggerLevels
        whitelist: DatagenConfig.TDatagenConfigTLoggerWhitelist

    class TDatagenConfigTEnvironmentNames(TypedDict, total=False):
        namespaces: dict[str, str]
        scoreboard: dict[str, str]
        dataStorage: dict[str, str]

    class TDatagenConfigTEnvironmentSettings(TypedDict, total=False):
        names: DatagenConfig.TDatagenConfigTEnvironmentNames

    class TDatagenConfig(TypedDict):
        builderSettings: DatagenConfig.TDatagenConfigTBuilderOptions
        dumperSettings: DatagenConfig.TDataGenConfigTDumperSettings
        loggerSettings: DatagenConfig.TDatagenConfigTLoggerSettings
        environmentSettings: DatagenConfig.TDatagenConfigTEnvironmentSettings
        
    config: TDatagenConfig

    __registered = False
    
    @staticmethod
    def register():
        if DatagenConfig.__registered: return
        DatagenConfig.__registered = True

        DatagenConfig.config = json.load(open(CONFIG_PATH, "r"))

DatagenConfig.register()