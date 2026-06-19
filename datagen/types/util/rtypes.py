from typing import Literal, LiteralString

from datagen.function.commands._data.datastorage import DataStorageValue
from datagen.function.commands.bossbar import BossBar
from datagen.function.function import Function
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.scoreboard.player import ScoreboardPlayer

type TInteger = (
    int 
    | str
    | LiteralString
    | DataStorageValue[int]
    | Function
    | FunctionMacroArgument[int]
    | ScoreboardPlayer
    | BossBar
)

type TFloat = (
    float
    | str
    | LiteralString
    | DataStorageValue[float]
    | Function
    | FunctionMacroArgument[float]
    | ScoreboardPlayer
    | BossBar
)
type TNumber = (
    TInteger
    | TFloat
)
type TString = (
    str
    | LiteralString
    | DataStorageValue[str | Identifier]
    | Function
    | FunctionMacroArgument[str | Identifier]
    | Identifier
)
type TIdentifier = (
    Identifier
    | str
    | LiteralString
    | DataStorageValue[Identifier]
    | Function
    | FunctionMacroArgument[Identifier]
)
type TFunction = (
    Function
    | FunctionMacroArgument[Function]
    | str
    | LiteralString
    | DataStorageValue[Identifier]
)
type TBool = (
    bool
    | str
    | Literal['True', 'False']
    | LiteralString
    | DataStorageValue[bool]
    | Function
    | FunctionMacroArgument[bool]
    | ScoreboardPlayer
    | BossBar
)
type TEntity = (
    str
    | LiteralString
    | DataStorageValue[str]
    | Function
    | FunctionMacroArgument[str]
    | TargetSelector
    | EntityType
)

type TAny = (
    TNumber
    | TString
    | TIdentifier
    | TFunction
    | TBool
    | TEntity
    | DataStorageValue[TAny]
)

type TPath = ( TString )