import json
from typing import TypedDict


FUNCTIONS_PATH = "function/"
TAGS_PATH = "tags/"
CONFIG_PATH = ".datagenconfig"

class DatagenConfig():
    class TDatagenConfigTBuilderOptions(TypedDict):
        source: str
        output: str
        indentation: int
    class TDataGenConfigTDumperSettings(TypedDict):
        source: str
        output: str

    class TDatagenConfig(TypedDict):
        builderSettings: DatagenConfig.TDatagenConfigTBuilderOptions
        dumperSettings: DatagenConfig.TDataGenConfigTDumperSettings
        
    config: TDatagenConfig

    __registered = False
    
    @staticmethod
    def register():
        if DatagenConfig.__registered: return
        DatagenConfig.__registered = True

        DatagenConfig.config = json.load(open(CONFIG_PATH, "r"))

DatagenConfig.register()