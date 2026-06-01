
from typing import final
from warnings import deprecated

from datagen.types.util.char import Char


@final
class Identifier():
    """
    Represents a Minecraft identifier, which is a string in the format "namespace:path". The namespace is usually the name of the mod or the game itself, while the path is the specific item, block, or other element being referenced.

    Example usage:
    ```
        id = Identifier.from_string("minecraft:stone")
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
    DEFAULT_NAMESPACE: str = "minecraft"

    @deprecated("Use of() method instead")
    def __init__(self):
        """
        Initializes a new Identifier instance.
        """
        self._namespace = ''
        self._path = ''

    def __str__(self) -> str:
        return f"{self._namespace}{~self.namespace_separator}{self._path}"
    
    def __list__(self) -> list[str]:
        return [self._namespace, self._path]
    
    def __repr__(self) -> str:
        return f"Identifier(namespace='{self._namespace}', path='{self._path}')"
    
    def equals(self, other: object) -> bool:
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
        return self.equals(other)
    
    @classmethod
    def from_string(cls, identifier: str) -> "Identifier":
        namespace, path = identifier.split(~cls.namespace_separator)
        return Identifier.of(namespace, path)

    @classmethod
    def of(cls, namespace: str, path: str) -> "Identifier":
        id = cls()
        id._namespace = namespace
        id._path = path
        return id
    
    def to_string(self) -> str:
        return str(self)
    
    def get_namespace(self) -> str:
        return self._namespace
    
    def get_path(self) -> str:
        return self._path
    
    def hash_code(self) -> int:
        return hash(str(self))