from pathlib import Path
from typing import TYPE_CHECKING, final
from typing_extensions import Self

from datagen.function.function import Function
from datagen.tag.functiontag import FunctionTag
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.logger import Logger

if TYPE_CHECKING:
    from datagen.predicate.predicate import Predicate
    from datagen.recipes.recipe import Recipe

@final
class Namespace:
    """
    # Namespace
    - See https://wiki.bedrock.dev/concepts/namespaces  
    (to Bedrock devs, but the concept is the same in Java)
    - See also https://minecraft.wiki/w/Identifier#Namespaces
    ## Summary
    Represents a Minecraft namespace, which is a way to organize and group
    resources in a datapack. Each namespace has a name and can contain
    functions, tags, predicates, and recipes. Namespaces are used to avoid
    naming conflicts between different datapacks and to provide a clear structure
    for resources. The Namespace class also manages a global set of all namespaces
    and the currently active namespace being built, allowing for easy retrieval
    of namespaces by name or identifier.

    ## Examples
    - Creating a Namespace and adding resources to it
    ```python
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.tag.itemtag import ItemTag
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text

def main():
    # Create a new datapack with the name "pack" and description "a pack"
    dp = DataPack("pack", "a pack")

    # Create a new namespace with the name "pack"
    ns = Namespace("pack")

    # Gets the minecraft namespace for adding resources to it
    mc = Namespace.minecraft

    # Create a new function with the identifier "pack:hello"
    with Function(ns / "hello") as f:
        # Add a command to the function that says "Hello, world!" to all players
        ~ Say("Hello, world!")

    # Add the function to the minecraft namespace's load tag, so it will
    # be executed when the datapack is loaded
    with ItemTag(ns / "coals") as t:
        # Add coal and charcoal to the tag using the `+=` operator, 
        # which allows for adding both individual items and other tags
        t += Items.COAL
        t += Items.CHARCOAL

    # Creates another function that will be added to the tick tag, which 
    # will be executed every game tick
    with Function(ns / "load") as f:
        # Add a command to the function that tells all players "Pack loaded!" 
        # when the datapack is loaded
        ~ TellRaw(
            TargetSelector.ALL_PLAYERS, # @a
            Text.literal("Pack loaded!") # { "text": "Pack loaded!" }
        )
        
        # Add the function to the minecraft namespace's load tag, 
        # so it will be executed when the datapack is loaded
        mc.load += f
        
    dp += ns
    dp.build()
```

    """

    minecraft: Namespace
    """The default Minecraft namespace, which contains all of the vanilla resources."""

    temp: Namespace
    """A temporary namespace that can be used for resources that don't need to be organized into a specific namespace."""

    instances: dict[str, Namespace]
    """A global dictionary of all namespace instances, keyed by their name. This allows for easy retrieval of namespaces by name."""

    name: str
    """The name of the namespace. This is used in resource identifiers and should be unique among all namespaces."""

    logger: Logger
    """A logger instance for the namespace, which can be used to log messages related to the namespace and its resources."""

    functions: set[Function]
    """A set of functions contained within the namespace."""

    tags: set[Tag]
    """A set of tags contained within the namespace."""

    predicates: set[Predicate]
    """A set of predicates contained within the namespace."""

    recipes: set[Recipe]
    """A set of recipes contained within the namespace."""

    load: FunctionTag
    """The load function tag for the namespace."""

    tick: FunctionTag
    """The tick function tag for the namespace."""

    def __new__(cls, name: str) -> Self: 
        ...
    def __init__(self, name: str) -> None: 
        ...

    @staticmethod
    def get_current_namespace() -> Namespace: 
        """Returns the currently active namespace being built. If no namespace is currently active, raises a ValueError."""
        ...

    @staticmethod
    def set_current_namespace(namespace: Namespace) -> None: 
        """Sets the currently active namespace being built to the given namespace."""
        ...

    @staticmethod
    def get(name: str | Identifier) -> Namespace: 
        """Returns the namespace with the given name or identifier. If no such namespace exists, creates a new namespace with the given name and returns it."""
        ...

    def identifier(self, path: str) -> Identifier: 
        """Returns an Identifier for a resource in the namespace with the given path. The identifier will have the namespace's name as its namespace, and the given path as its path."""
        ...

    def add(self, obj: Function | Tag | Predicate) -> Self: 
        """Adds a function, tag, or predicate to the namespace. The resource's namespace is set to this namespace, and its identifier is updated accordingly. The resource is also added to the appropriate set of resources in the namespace."""
        ...

    def add_function(self, function: Function) -> Self: 
        """Adds a function to the namespace. The function's namespace is set to this namespace, and its identifier is updated accordingly. The function is also added to the set of functions in the namespace."""
        ...

    def add_tag(self, tag: Tag) -> Self: 
        """Adds a tag to the namespace. The tag's namespace is set to this namespace, and its identifier is updated accordingly. The tag is also added to the set of tags in the namespace."""
        ...

    def add_predicate(self, predicate: Predicate) -> Self: 
        """Adds a predicate to the namespace. The predicate's namespace is set to this namespace, and its identifier is updated accordingly. The predicate is also added to the set of predicates in the namespace."""
        ...

    def add_recipe(self, recipe: Recipe) -> Self: 
        """Adds a recipe to the namespace. The recipe's namespace is set to this namespace, and its identifier is updated accordingly. The recipe is also added to the set of recipes in the namespace."""
        ...

    def add_recipes(self, *recipes: Recipe) -> Self: 
        """Adds multiple recipes to the namespace. Each recipe's namespace is set to this namespace, and its identifier is updated accordingly. The recipes are also added to the set of recipes in the namespace."""
        ...

    def add_tags(self, *tags: Tag) -> Self: 
        """Adds multiple tags to the namespace. Each tag's namespace is set to this namespace, and its identifier is updated accordingly. The tags are also added to the set of tags in the namespace."""
        ...

    def build_functions(self, base: Path) -> None: 
        """Builds the functions in the namespace into the appropriate subdirectory of the output directory. Each function is built into a separate file with the same name as the function's identifier, and the necessary folder structure is created if it doesn't already exist."""
        ...

    def build_tags(self, base: Path) -> None: 
        """Builds the tags in the namespace into the appropriate subdirectory of the output directory. Each tag is built into a separate file with the same name as the tag's identifier, and the necessary folder structure is created if it doesn't already exist."""
        ...

    def build_predicates(self, base: Path) -> None: 
        """Builds the predicates in the namespace into the appropriate subdirectory of the output directory. Each predicate is built into a separate file with the same name as the predicate's identifier, and the necessary folder structure is created if it doesn't already exist."""
        ...

    def build_recipes(self, base: Path) -> None: 
        """Builds the recipes in the namespace into the appropriate subdirectory of the output directory. Each recipe is built into a separate file with the same name as the recipe's identifier, and the necessary folder structure is created if it doesn't already exist."""
        ...

    def build(self, base: Path) -> None: 
        """Builds all resources in the namespace into the appropriate subdirectories of the output directory."""
        ...

    def __truediv__(self, path: str) -> Identifier: 
        """Returns an Identifier for a resource in the namespace with the given path. This allows for a convenient syntax for creating identifiers, where `namespace / "path/to/resource"` is equivalent to `namespace.identifier("path/to/resource")`."""
        ...

    def __enter__(self) -> Self: 
        """Sets this namespace as the currently active namespace being built, and returns the namespace for use in a with statement. This allows for a convenient syntax for building resources within a namespace, where `with namespace:` can be used to set the active namespace for the duration of the block."""
        ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: 
        """Exits the context of the namespace, clearing the currently active namespace being built. This is called automatically at the end of a with block that uses the namespace as a context manager."""
        ...

    def __iadd__(self, other: Function | Tag | "Predicate") -> Self: 
        """Adds a resource to the namespace using the `+=` operator."""
        ...