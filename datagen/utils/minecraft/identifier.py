
from typing import final, overload, override
from warnings import deprecated

from datagen.types.util.char import Char


@final
class Identifier():
    """
    # Identifier
    - See https://minecraft.wiki/w/Identifier
    ## Summary
    Represents a Minecraft identifier, which is a string in the format "namespace:path". The namespace is usually the name of the mod or the game itself, while the path is the specific item, block, or other element being referenced.

    ## Example
    ```
        id = Identifier.of("minecraft:stone")
        print(id)  # Output: minecraft:stone
        print(id.get_namespace())  # Output: minecraft
        print(id.get_path())  # Output: stone
    ```
    ```
        id = Identifier.of("minecraft", "stone")
        print(id)  # Output: minecraft:stone
        print(id.get_namespace())  # Output: minecraft
        print(id.get_path())  # Output: stone
    ```
    """
    namespace_separator: Char = Char(':')
    """The character used to separate the namespace and path in a Minecraft identifier. By default, this is a colon (':'), but it can be changed if needed. For example, if you wanted to use a different separator, you could set `Identifier.namespace_separator = Char('/')`, and then identifiers would be in the format "namespace/path" instead of "namespace:path"."""
    DEFAULT_NAMESPACE: str = "minecraft"
    """The default namespace used when creating identifiers without specifying a namespace. This is typically set to "minecraft", which is the namespace used for all vanilla Minecraft resources. For example, if you create an identifier with `Identifier.of("stone")`, it will automatically use the default namespace and create an identifier with the value "minecraft:stone"."""

    @deprecated("Use of() method instead")
    def __init__(self):
        self._namespace = ''
        self._path = ''

    def __str__(self) -> str:
        """Returns the string representation of the identifier in the format "namespace:path". The namespace and path are converted to lowercase to ensure consistency, as Minecraft identifiers are case-insensitive. For example, if the namespace is "Minecraft" and the path is "Stone", the resulting string will be "minecraft:stone"."""
        return f"{self._namespace}{~self.namespace_separator}{self._path}".lower()
    
    def __list__(self) -> list[str]:
        """Returns a list representation of the identifier, where the first element is the namespace and the second element is the path. This can be useful for certain operations where you want to work with the namespace and path separately. For example, if the identifier is "minecraft:stone", this method will return ["minecraft", "stone"]."""
        return [self._namespace, self._path]
    
    def __repr__(self) -> str:
        """Returns a string representation of the identifier that includes both the namespace and path in a clear format. This is useful for debugging and logging purposes, as it provides a more detailed view of the identifier's components. For example, if the identifier is "minecraft:stone", this method will return "Identifier(namespace='minecraft', path='stone')", which clearly shows the namespace and path values."""
        return f"Identifier(namespace='{self._namespace}', path='{self._path}')"
    
    def equals(self, other: object) -> bool:
        """Compares the identifier to another object for equality. The method supports comparing the identifier to a string, a list, a tuple, or another Identifier instance. When comparing to a string, it checks if the string representation of the identifier matches the given string. When comparing to a list or tuple, it checks if the namespace and path match the corresponding elements in the list or tuple. When comparing to another Identifier instance, it checks if both the namespace and path are the same. For example, if the identifier is "minecraft:stone", it will be equal to the string "minecraft:stone", the list ["minecraft", "stone"], the tuple ("minecraft", "stone"), and another Identifier instance with the same namespace and path."""
        if isinstance(other, str):
            return str(self) == other
        
        elif isinstance(other, list):
            return [self._namespace, self._path] == other

        elif isinstance(other, tuple) and len(other) == 2:
            return (self._namespace, self._path) == other
        
        elif isinstance(other, Identifier):
            return self._namespace == other._namespace and self._path == other._path
        
        return False
    
    def __eq__(self, other: object) -> bool:
        """Overrides the equality operator to compare the identifier to another object using the equals() method. This allows you to use the `==` operator to compare an Identifier instance to a string, list, tuple, or another Identifier instance, and it will return True if they are considered equal based on the criteria defined in the equals() method. For example, if you have an Identifier instance representing "minecraft:stone", you can compare it to the string "minecraft:stone" using `identifier == "minecraft:stone"`, and it will return True."""
        return self.equals(other)
    
    @classmethod
    def from_string(cls, identifier: str) -> "Identifier":
        """Creates an Identifier instance from a string in the format "namespace:path". The string is split into the namespace and path components, and a new Identifier instance is created with these values."""
        namespace, path = identifier.split(~cls.namespace_separator)
        return Identifier.of(namespace, path)

    @overload
    @classmethod
    def of(cls, identifier: str, /) -> "Identifier": 
        """Creates an Identifier instance from a single string in the format "namespace:path". The string is parsed to extract the namespace and path, and a new Identifier instance is created with these values. For example, if you call `Identifier.of("minecraft:stone")`, it will create an Identifier instance with the namespace "minecraft" and the path "stone"."""
        ...

    @overload
    @classmethod
    def of(cls, namespace: str, path: str, /) -> "Identifier": 
        """Creates an Identifier instance from either a single string in the format "namespace:path" or from separate namespace and path strings. If a single string is provided, it is parsed to extract the namespace and path. If two strings are provided, they are used directly as the namespace and path. This method provides flexibility in how you can create Identifier instances, allowing for both concise and explicit creation depending on your needs. For example, you can create an identifier with `Identifier.of("minecraft:stone")` or with `Identifier.of("minecraft", "stone")`, and both will result in an Identifier instance representing "minecraft:stone"."""
        ...

    @classmethod
    def of(cls, *a) -> "Identifier":
        """Creates an Identifier instance from either a single string in the format "namespace:path" or from separate namespace and path strings. If a single string is provided, it is parsed to extract the namespace and path. If two strings are provided, they are used directly as the namespace and path. This method provides flexibility in how you can create Identifier instances, allowing for both concise and explicit creation depending on your needs. For example, you can create an identifier with `Identifier.of("minecraft:stone")` or with `Identifier.of("minecraft", "stone")`, and both will result in an Identifier instance representing "minecraft:stone"."""
        if len(a) == 1:
            return cls.from_string(a[0])
        
        elif len(a) == 2:
            namespace, path = a
            id = cls()
            id._namespace = namespace
            id._path = path
            return id
        
        else:
            raise ValueError("Invalid number of arguments for Identifier.of() method. Expected 1 or 2, got {len(a)}.")
    
    def to_string(self) -> str:
        """
        Converts the Identifier instance to its string representation in the format "namespace:path". This is useful for when you need to use the identifier as a string, such as when writing it to a file or using it in a context where a string is required. For example, if you have an Identifier instance representing "minecraft:stone", calling `to_string()` on it will return the string "minecraft:stone".
        """
        return str(self)
    
    def get_namespace(self) -> str:
        """
        Returns the namespace component of the identifier. The namespace is the part of the identifier that comes before the separator (usually a colon) and is used to group related resources together. For example, in the identifier "minecraft:stone", the namespace is "minecraft". This method allows you to access just the namespace portion of the identifier if you need to work with it separately from the path.
        """
        return self._namespace
    
    def get_path(self) -> str:
        """
        Returns the path component of the identifier. The path is the part of the identifier that comes after the separator (usually a colon) and specifies the specific item, block, or other element being referenced. For example, in the identifier "minecraft:stone", the path is "stone". This method allows you to access just the path portion of the identifier if you need to work with it separately from the namespace.
        """
        return self._path
    
    def __invert__(self):
        """Returns the string representation of the identifier. This allows you to use the `~` operator to get the string form of the identifier, which can be convenient in certain contexts. For example, if you have an Identifier instance representing "minecraft:stone", using `~identifier` will return the string "minecraft:stone"."""
        return str(self)
    
    def __hash__(self) -> int:
        """Returns a hash value for the identifier, which is based on its string representation. This allows Identifier instances to be used as keys in dictionaries or stored in sets, as they will have a consistent hash value based on their namespace and path. For example, if you have two Identifier instances that both represent "minecraft:stone", they will have the same hash value, allowing them to be treated as equal in sets and dictionaries."""
        return hash(str(self))