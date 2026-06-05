from datagen.types.util.min import Range
from datagen.utils.repr.biome import Biome
from datagen.utils.repr.block import Block


class LocationPredicate():
    def __init__(self) -> None:
        self._data: dict = {}

    def with_biome(self, biome: Biome) -> "LocationPredicate":
        self._data["biomes"] = [str(biome.id)]
        return self

    def with_block(self, block: Block) -> "LocationPredicate":
        self._data["block"] = {"blocks": [str(block.id)]}
        return self

    def with_dimension(self, dimension: str) -> "LocationPredicate":
        self._data["dimension"] = dimension
        return self

    def with_light(self, light: Range) -> "LocationPredicate":
        self._data["light"] = {"light": {"min": light.start, "max": light.end}}
        return self

    def with_smokey(self, smokey: bool = True) -> "LocationPredicate":
        self._data["smokey"] = smokey
        return self

    def with_position(self, x: Range | None = None, y: Range | None = None, z: Range | None = None) -> "LocationPredicate":
        position: dict = {}
        if x is not None:
            position["x"] = {"min": x.start, "max": x.end}
        if y is not None:
            position["y"] = {"min": y.start, "max": y.end}
        if z is not None:
            position["z"] = {"min": z.start, "max": z.end}

        if position:
            self._data["position"] = position

        return self

    def set(self, key: str, value) -> "LocationPredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
