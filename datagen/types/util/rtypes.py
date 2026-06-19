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
"""
A Type to represent Integers in the datagen library. 
It can be an int, a str, a LiteralString, a 
DataStorageValue[int], a Function, a FunctionMacroArgument[int], 
a ScoreboardPlayer, or a BossBar.

how?  
- int, str or LiteralString: for constant values
>>> 1, '2', "3" 
- DataStorageValue[int]: for values stored in a data storage
>>> DataStorage(...)['path']['to']['value'][int]
- Function: for values returned by a function
>>> ~ Return(0)
- FunctionMacroArgument[int]: for values passed as arguments to a function
>>> f = Function(...)
>>> i = f['i'][int] # i is a FunctionMacroArgument[int]

- ScoreboardPlayer: for values stored in a scoreboard objective
- BossBar: for values stored in a bossbar
"""

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
"""
A Type to represent Floats in the datagen library.
It can be a float, a str, a LiteralString, a
DataStorageValue[float], a Function, a FunctionMacroArgument[float],
a ScoreboardPlayer, or a BossBar.

how?
- float, str or LiteralString: for constant values
>>> 1.5, '2.0', "3.14"
- DataStorageValue[float]: for values stored in a data storage
>>> DataStorage(...)['path']['to']['value'][float]
- Function: for values returned by a function
>>> ~ Return(1.5)
- FunctionMacroArgument[float]: for values passed as arguments to a function
>>> f = Function(...)
>>> i = f['i'][float] # i is a FunctionMacroArgument[float]

- ScoreboardPlayer: for values stored in a scoreboard objective
- BossBar: for values stored in a bossbar
"""
type TNumber = (
    TInteger
    | TFloat
)
"""
A Type to represent Numbers in the datagen library.
It is a union of TInteger and TFloat, covering all numeric types.

how?
- TInteger: for integer values
- TFloat: for floating-point values
"""
type TString = (
    str
    | LiteralString
    | DataStorageValue[str | Identifier]
    | Function
    | FunctionMacroArgument[str | Identifier]
    | Identifier
)
"""
A Type to represent Strings in the datagen library.
It can be a str, a LiteralString, a DataStorageValue[str | Identifier],
a Function, a FunctionMacroArgument[str | Identifier], or an Identifier.

how?
- str or LiteralString: for constant string values
>>> "hello", 'world'
- DataStorageValue[str | Identifier]: for strings stored in a data storage
>>> DataStorage(...)['path']['to']['value'][str]
- Function: for strings returned by a function
>>> ~ Return('hello')
- FunctionMacroArgument[str | Identifier]: for strings passed as arguments
>>> f = Function(...)
>>> s = f['s'][str] # s is a FunctionMacroArgument[str]

- Identifier: for Minecraft identifiers like 'minecraft:stone'
"""
type TIdentifier = (
    Identifier
    | str
    | LiteralString
    | DataStorageValue[Identifier]
    | Function
    | FunctionMacroArgument[Identifier]
)
"""
A Type to represent Minecraft Identifiers in the datagen library.
It can be an Identifier, a str, a LiteralString, a
DataStorageValue[Identifier], a Function, or a
FunctionMacroArgument[Identifier].

how?
- Identifier: for direct Minecraft identifiers
>>> Identifier('minecraft:stone')
- str or LiteralString: for constant identifier values
>>> 'minecraft:stone', "minecraft:diamond"
- DataStorageValue[Identifier]: for identifiers stored in a data storage
>>> DataStorage(...)['path']['to']['value'][Identifier]
- Function: for identifiers returned by a function
>>> ~ Return('minecraft:stone')
- FunctionMacroArgument[Identifier]: for identifiers passed as arguments
>>> f = Function(...)
>>> id = f['id'][Identifier] # id is a FunctionMacroArgument[Identifier]
"""
type TFunction = (
    Function
    | FunctionMacroArgument[Function]
    | str
    | LiteralString
    | DataStorageValue[Identifier]
)
"""
A Type to represent Functions in the datagen library.
It can be a Function, a FunctionMacroArgument[Function], a str,
a LiteralString, or a DataStorageValue[Identifier].

how?
- Function: for direct function references
>>> Function('namespace:path')
- FunctionMacroArgument[Function]: for functions passed as arguments
>>> f = Function(...)
>>> fn = f['fn'][Function] # fn is a FunctionMacroArgument[Function]
- str or LiteralString: for constant function names
>>> 'namespace:path', "namespace:path"
- DataStorageValue[Identifier]: for functions stored in a data storage
>>> DataStorage(...)['path']['to']['value'][Identifier]
"""
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
"""
A Type to represent Booleans in the datagen library.
It can be a bool, a str, a Literal['True', 'False'], a LiteralString,
a DataStorageValue[bool], a Function, a FunctionMacroArgument[bool],
a ScoreboardPlayer, or a BossBar.

how?
- bool: for constant boolean values
>>> True, False
- str or Literal['True', 'False'] or LiteralString: for constant string booleans
>>> 'True', "False"
- DataStorageValue[bool]: for booleans stored in a data storage
>>> DataStorage(...)['path']['to']['value'][bool]
- Function: for booleans returned by a function
>>> ~ Return(True)
- FunctionMacroArgument[bool]: for booleans passed as arguments
>>> f = Function(...)
>>> b = f['b'][bool] # b is a FunctionMacroArgument[bool]

- ScoreboardPlayer: for values stored in a scoreboard objective
- BossBar: for values stored in a bossbar
"""
type TEntity = (
    str
    | LiteralString
    | DataStorageValue[str]
    | Function
    | FunctionMacroArgument[str]
    | TargetSelector
    | EntityType
)
"""
A Type to represent Entities in the datagen library.
It can be a str, a LiteralString, a DataStorageValue[str],
a Function, a FunctionMacroArgument[str], a TargetSelector,
or an EntityType.

how?
- str or LiteralString: for constant entity selectors or names
>>> '@p', '@a[sort=nearest]', 'PlayerName'
- DataStorageValue[str]: for entity strings stored in a data storage
>>> DataStorage(...)['path']['to']['value'][str]
- Function: for entity selectors returned by a function
>>> ~ Return('@p')
- FunctionMacroArgument[str]: for entity strings passed as arguments
>>> f = Function(...)
>>> e = f['e'][str] # e is a FunctionMacroArgument[str]
- TargetSelector: for Minecraft target selectors
>>> TargetSelector('@p')
- EntityType: for Minecraft entity types
>>> EntityType('minecraft:zombie')
"""
type TAny = (
    TNumber
    | TString
    | TIdentifier
    | TFunction
    | TBool
    | TEntity
    | DataStorageValue[TAny]
)
"""
A Type to represent any value in the datagen library.
It is a union of all other types:
TNumber, TString, TIdentifier, TFunction, TBool, TEntity,
and recursively DataStorageValue[TAny].

how?
- TNumber: any numeric value (integer or float)
- TString: any string value
- TIdentifier: any Minecraft identifier
- TFunction: any function reference
- TBool: any boolean value
- TEntity: any entity selector or type
- DataStorageValue[TAny]: any value stored in a data storage
>>> DataStorage(...)['path']['to']['value'][TAny]
"""

type TPath = ( TString )
"""
A Type to represent Paths in the datagen library.
It is an alias for TString, representing file or resource paths.

how?
- TString: any string value can be used as a path
>>> 'namespace:path/to/file', "path/to/function"
"""