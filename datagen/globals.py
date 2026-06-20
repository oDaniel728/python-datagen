import json
from typing import TypedDict


FUNCTIONS_PATH = "function/"
TAGS_PATH = "tags/"
PREDICATES_PATH = "predicate/"
RECIPES_PATH = "recipe/"
ADVANCEMENTS_PATH = "advancement/"
CONFIG_PATH = ".datagenconfig"

class DatagenConfig():
    class TDatagenConfigTBuilderOptions(TypedDict):
        source: str
        output: str
        indent: int
        comment: bool
        allowEmptyLines: bool
        obfuscate: bool
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

    class TDatagenConfigTLoggerSettings(TypedDict):
        enabled: bool
        levels: DatagenConfig.TDatagenConfigTLoggerLevels

    class TDatagenConfig(TypedDict):
        builderSettings: DatagenConfig.TDatagenConfigTBuilderOptions
        dumperSettings: DatagenConfig.TDataGenConfigTDumperSettings
        loggerSettings: DatagenConfig.TDatagenConfigTLoggerSettings
        
    config: TDatagenConfig

    __registered = False
    
    @staticmethod
    def register():
        if DatagenConfig.__registered: return
        DatagenConfig.__registered = True

        DatagenConfig.config = json.load(open(CONFIG_PATH, "r"))

DatagenConfig.register()