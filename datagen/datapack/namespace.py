from pathlib import Path
from typing import TYPE_CHECKING
from typing import final
from uuid import uuid4
from typing_extensions import Self

from datagen.advancement.advancement import Advancement
from datagen.function.function import Function
from datagen.tag.functiontag import FunctionTag
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.logger import Logger

if TYPE_CHECKING:
    from datagen.predicate.predicate import Predicate
    from datagen.recipes.recipe import Recipe
    from datagen.utils.repr.enchantment_provider import EnchantmentProvider

_current_namespace: Namespace
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
    mc = Namespace.minecraft()

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

    name: str
    """The name of the namespace. This is used in resource identifiers and should be unique among all namespaces."""

    logger: Logger
    """A logger instance for the namespace, which can be used to log messages related to the namespace and its resources."""

    functions: set[Function]
    """A set of functions contained within the namespace."""

    tags: set[Tag]
    """A set of tags contained within the namespace."""

    predicates: set["Predicate"]
    """A set of predicates contained within the namespace."""

    recipes: set["Recipe"]
    """A set of recipes contained within the namespace."""

    load: FunctionTag
    """The load function tag for the namespace."""

    tick: FunctionTag
    """The tick function tag for the namespace."""

    @staticmethod
    def get_current_namespace() -> "Namespace":
        """Returns the currently active namespace being built. If no namespace is currently active, raises a ValueError."""
        return _current_namespace

    @staticmethod
    def set_current_namespace(namespace: "Namespace") -> None:
        """Sets the currently active namespace being built to the given namespace."""
        global _current_namespace
        _current_namespace = namespace


    def __init__(self, name: str) -> None:
        self.name = name

        self.logger = Logger(name)

        self.functions = set[Function]()
        self.tags = set[Tag]()
        self.predicates = set["Predicate"]()
        self.recipes = set["Recipe"]()
        self.enchantments = set["EnchantmentProvider"]()

        self.load = FunctionTag(self / "load", [])
        self.tick = FunctionTag(self / "tick", [])
        self.add_tags(self.load, self.tick)

    def identifier(self, path: str) -> Identifier:
        """Returns an Identifier for a resource in the namespace with the given path. The identifier will have the namespace's name as its namespace, and the given path as its path."""
        return Identifier.from_string(f"{self.name}:{path}")

    def add(self, obj: Function | Tag | "Predicate" | "EnchantmentProvider") -> Self:
        """Adds a function, tag, predicate, or enchantment to the namespace. The resource's namespace is set to this namespace, and its identifier is updated accordingly. The resource is also added to the appropriate set of resources in the namespace."""
        from datagen.predicate.predicate import Predicate
        from datagen.utils.repr.enchantment_provider import EnchantmentProvider as EP

        if isinstance(obj, Function):
            return self.add_function(obj)
        elif isinstance(obj, Tag):
            return self.add_tag(obj)
        elif isinstance(obj, Predicate):
            return self.add_predicate(obj)
        elif isinstance(obj, EP):
            return self.add_enchantment(obj)
        else:
            raise TypeError(f"Object of type '{type(obj)}' is not a Function, Tag or Predicate")

    def add_function(self, function: Function) -> Self:
        """Adds a function to the namespace. The function's namespace is set to this namespace, and its identifier is updated accordingly. The function is also added to the set of functions in the namespace."""
        self.logger.info(f"Adding function '{function.id._path}' to namespace '{self.name}'")
        function.namespace = self # type: ignore
        self.functions.add(function)
        return self

    def add_tag(self, tag: Tag) -> Self:
        """Adds a tag to the namespace. The tag's namespace is set to this namespace, and its identifier is updated accordingly. The tag is also added to the set of tags in the namespace."""
        self.logger.info(f"Adding tag '{tag.id._path}' to namespace '{self.name}'")
        tag.namespace = self # type: ignore
        self.tags.add(tag)
        return self

    def add_predicate(self, predicate: "Predicate") -> Self:
        """Adds a predicate to the namespace. The predicate's namespace is set to this namespace, and its identifier is updated accordingly. The predicate is also added to the set of predicates in the namespace."""
        self.logger.info(f"Adding predicate '{predicate.id._path}' to namespace '{self.name}'")
        predicate.namespace = self # type: ignore
        self.predicates.add(predicate)
        return self

    def add_recipe(self, recipe: "Recipe") -> Self:
        """Adds a recipe to the namespace. The recipe's namespace is set to this namespace, and its identifier is updated accordingly. The recipe is also added to the set of recipes in the namespace."""
        self.logger.info(f"Adding recipe '{recipe.id._path}' to namespace '{self.name}'")
        recipe.namespace = self # type: ignore
        recipe.id._namespace = self.name
        self.recipes.add(recipe)
        return self

    def add_recipes(self, *recipes: "Recipe") -> Self:
        """Adds multiple recipes to the namespace. Each recipe's namespace is set to this namespace, and its identifier is updated accordingly. The recipes are also added to the set of recipes in the namespace."""
        for recipe in recipes:
            self.add_recipe(recipe)
        return self

    def add_tags(self, *tags: Tag) -> Self:
        """Adds multiple tags to the namespace. Each tag's namespace is set to this namespace, and its identifier is updated accordingly. The tags are also added to the set of tags in the namespace."""
        for tag in tags:
            self.add_tag(tag)
        return self

    def add_advancement(self, adv: "Advancement") -> Self:
        """Adds an advancement to the namespace. The advancement's namespace is set to this namespace, and its identifier is updated accordingly. The advancement is also added to the set of advancements in the namespace."""
        self.logger.info(f"Adding advancement '{adv.id._path}' to namespace '{self.name}'")
        adv._ns = self # type: ignore
        return self

    def add_advancements(self, *advs: "Advancement") -> Self:
        """Adds multiple advancements to the namespace. Each advancement's namespace is set to this namespace, and its identifier is updated accordingly. The advancements are also added to the set of advancements in the namespace."""
        for adv in advs:
            self.add_advancement(adv)
        return self

    def add_enchantment(self, enchantment: "EnchantmentProvider") -> Self:
        """Adds an enchantment to the namespace. The enchantment's namespace is set to this namespace, and its identifier is updated accordingly."""
        self.logger.info(f"Adding enchantment '{enchantment.id._path}' to namespace '{self.name}'")
        enchantment.namespace = self
        self.enchantments.add(enchantment)
        return self

    def add_enchantments(self, *enchantments: "EnchantmentProvider") -> Self:
        """Adds multiple enchantments to the namespace. Each enchantment's namespace is set to this namespace, and its identifier is updated accordingly."""
        for e in enchantments:
            self.add_enchantment(e)
        return self

    def build_functions(self, base: Path) -> None:
        """Builds the functions in the namespace into the appropriate subdirectory of the output directory. Each function is built into a separate file with the same name as the function's identifier, and the necessary folder structure is created if it doesn't already exist."""
        Logger.start_task(f"Building functions in namespace '{self.name}'")
        for function in self.functions:
            self.logger.info(f"Building function '{function.id._path}' in namespace '{self.name}'")
            f = function.to_file()
            f.build(base)
        Logger.end_task(f"Building functions in namespace '{self.name}'")

    def build_tags(self, base: Path) -> None:
        """Builds the tags in the namespace into the appropriate subdirectory of the output directory. Each tag is built into a separate file with the same name as the tag's identifier, and the necessary folder structure is created if it doesn't already exist."""
        Logger.start_task(f"Building tags in namespace '{self.name}'")
        for tag in self.tags:
            self.logger.info(f"Building tag '{tag.id._path}' in namespace '{self.name}'")
            if tag.values.__len__() == 0:
                continue
            f = tag.to_file()
            f.build(base)
        Logger.end_task(f"Building tags in namespace '{self.name}'")

    def build_predicates(self, base: Path) -> None:
        """Builds the predicates in the namespace into the appropriate subdirectory of the output directory. Each predicate is built into a separate file with the same name as the predicate's identifier, and the necessary folder structure is created if it doesn't already exist."""
        Logger.start_task(f"Building predicates in namespace '{self.name}'")
        for predicate in self.predicates:
            self.logger.info(f"Building predicate '{predicate.id._path}' in namespace '{self.name}'")
            f = predicate.to_file()
            f.build(base)
        Logger.end_task(f"Building predicates in namespace '{self.name}'")

    def build_advancements(self, base: Path) -> None:
        Logger.start_task(f"Building advancements in namespace '{self.name}'")
        for adv in Advancement.advancements.values():
            if adv._ns != self:
                continue
            self.logger.info(f"Building advancement '{adv.id._path}' in namespace '{self.name}'")
            f = adv.to_file()
            f.build(base)
        Logger.end_task(f"Building advancements in namespace '{self.name}'")

    def build_recipes(self, base: Path) -> None:
        """Builds the recipes in the namespace into the appropriate subdirectory of the output directory. Each recipe is built into a separate file with the same name as the recipe's identifier, and the necessary folder structure is created if it doesn't already exist."""
        Logger.start_task(f"Building recipes in namespace '{self.name}'")
        for recipe in self.recipes:
            self.logger.info(f"Building recipe '{recipe.id._path}' in namespace '{self.name}'")
            f = recipe.to_file()
            f.build(base)
        Logger.end_task(f"Building recipes in namespace '{self.name}'")

    def build_enchantments(self, base: Path) -> None:
        """Builds the enchantments in the namespace into the appropriate subdirectory of the output directory."""
        Logger.start_task(f"Building enchantments in namespace '{self.name}'")
        for enchantment in self.enchantments:
            self.logger.info(f"Building enchantment '{enchantment.id._path}' in namespace '{self.name}'")
            f = enchantment.to_file()
            f.build(base)
        Logger.end_task(f"Building enchantments in namespace '{self.name}'")

    def build(self, base: Path) -> None:
        """Builds all resources in the namespace into the appropriate subdirectories of the output directory."""
        Logger.start_task(f"Building namespace '{self.name}'")
        self.build_functions(base)
        self.build_tags(base)
        self.build_predicates(base)
        self.build_advancements(base)
        self.build_recipes(base)
        self.build_enchantments(base)
        Logger.end_task(f"Building namespace '{self.name}'")

    def __truediv__(self, path: str) -> Identifier:
        """Returns an Identifier for a resource in the namespace with the given path. This allows for a convenient syntax for creating identifiers, where `namespace / "path/to/resource"` is equivalent to `namespace.identifier("path/to/resource")`."""
        return self.identifier(path)

    def __enter__(self) -> Self:
        """Sets this namespace as the currently active namespace being built, and returns the namespace for use in a with statement. This allows for a convenient syntax for building resources within a namespace, where `with namespace:` can be used to set the active namespace for the duration of the block."""
        self.set_current_namespace(self)
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        """Exits the context of the namespace, clearing the currently active namespace being built. This is called automatically at the end of a with block that uses the namespace as a context manager."""
        self.set_current_namespace(None) # type: ignore

    type _TAddition = Function | Tag | "Predicate" | "EnchantmentProvider"
    def __iadd__(self, other: _TAddition | tuple[_TAddition, ...]) -> Self:
        """Adds a resource to the namespace using the `+=` operator."""
        if isinstance(other, tuple):
            for item in other:
                self += item
        else:
            self.add(other)
        return self

    def __invert__(self):
        from datagen.datapack.datapack import DataPack
        dp = DataPack.get_current_datapack()
        dp += self
        return self

    @staticmethod
    def minecraft() -> "Namespace":
        """Returns the default Minecraft namespace, which contains all of the vanilla resources."""
        return Namespace('minecraft')
    
    _TEMP: "Namespace | None" = None

    @staticmethod
    def temp() -> "Namespace":
        """Returns a temporary namespace that can be used for resources that don't need to be organized into a specific namespace."""
        return Namespace("temp")
    