from datagen.types.util.min import Range
from datagen.types.util.validpredicate import ValidPredicate
from datagen.utils._dictify import dictify
from datagen.utils.repr.biome import Biome
from datagen.utils.repr.block import Block
from datagen.utils.snbtserializer import SNBTSerializer


class LocationPredicate(ValidPredicate):
    def __init__(self) -> None:
        self._data: dict = {}

    def with_biomes(self, *biomes: Biome) -> "LocationPredicate":
        self._data["biomes"] = [str(biome.id) for biome in biomes]
        return self

    def with_blocks(self, *blocks: Block, state: dict | None = None, nbt: dict | None = None, components: dict | None = None) -> "LocationPredicate":
        self._data["block"] = {"blocks": [str(block.id) for block in blocks]}
        if state is not None:
            self._data["block"]["state"] = dictify(state) # type: ignore
        if nbt is not None:
            self._data["block"]["nbt"] = SNBTSerializer.serialize(nbt) # type: ignore
        if components is not None:
            self._data["block"]["components"] = dictify(components) # type: ignore
        
        return self

    def with_dimension(self, dimension: str) -> "LocationPredicate":
        self._data["dimension"] = dimension
        return self

    def with_light(self, light: Range | int) -> "LocationPredicate":
        if isinstance(light, int):
            self._data["light"] = {"light": light}
        else:
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
