from datagen.globals import DatagenConfig


class Obfuscator():
    _map: dict[str, str] = {}
    _counter: int = 0

    @classmethod
    def obfuscate(cls, name: str) -> str:
        if not DatagenConfig.config["builderSettings"].get("obfuscate", False):
            return name
        if name not in cls._map:
            cls._map[name] = cls._generate()
        return cls._map[name]

    @classmethod
    def obfuscate_path(cls, namespace: str, path: str) -> str:
        if not DatagenConfig.config["builderSettings"].get("obfuscate", False):
            return path
        if namespace != "temp":
            return path
        return cls.obfuscate(path)

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
