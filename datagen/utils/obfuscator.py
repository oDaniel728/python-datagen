from datagen.globals import DatagenConfig
from datagen.utils.environment import Environment


class Obfuscator():
    _map: dict[str, str] = {}
    _counter: int = 0

    @staticmethod
    def _obfuscation_config() -> DatagenConfig.TDatagenConfigTObfuscation:
        return DatagenConfig.config["builderSettings"].get("obfuscation", {})

    @classmethod
    def _is_enabled(cls, category: str | None = None) -> bool:
        """Checks whether obfuscation is enabled for a given category.

        *category* is a dotted path into ``obfuscation.where``, e.g.
        ``"identifiers.functions"`` or ``"other.scoreboard.objectives"``.
        If *category* is `None`, only the top-level ``enabled`` flag is checked.
        """
        config = cls._obfuscation_config()
        if not config.get("enabled", False):
            return False
        if category is None:
            return True
        node = config.get("where", {})
        for part in category.split("."):
            if not isinstance(node, dict):
                return False
            node = node.get(part)
            if node is None:
                return False
        return bool(node)

    @classmethod
    def obfuscate(cls, name: str, category: str | None = None) -> str:
        if not cls._is_enabled(category):
            return name
        if name not in cls._map:
            cls._map[name] = cls._generate()
        return cls._map[name]

    @classmethod
    def obfuscate_path(cls, namespace: str, path: str, category: str | None = None) -> str:
        if not cls._is_enabled(category):
            return path
        if namespace != Environment.namespace_temp():
            return path
        return cls.obfuscate(path, category)

    @classmethod
    def _generate(cls) -> str:
        n = cls._counter
        cls._counter += 1
        result = "_"
        while True:
            result += chr(ord('a') + (n % 26))
            n //= 26
            if n == 0:
                break
        return result

    @classmethod
    def reset(cls) -> None:
        cls._map.clear()
        cls._counter = 0
