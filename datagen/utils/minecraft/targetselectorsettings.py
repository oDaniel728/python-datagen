from typing import TYPE_CHECKING, Any, Literal

from datagen.advancement.advancement import Advancement
if TYPE_CHECKING: from datagen.entitytag import EntityTag
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.snbtserializer import SNBTSerializer


class TargetSelectorSettings():

    TSort = Literal[
        "nearest",
        "furthest",
        "random",
        "arbitrary"
    ]

    TGamemode = Literal[
        "survival",
        "creative",
        "adventure",
        "spectator"
    ]    

    def __init__(self,
        *,
        
        # Position
        x: int | Range | None = None,
        y: int | Range | None = None,
        z: int | Range | None = None,
        
        # Volume
        dx: int | Range | None = None,
        dy: int | Range | None = None,
        dz: int | Range | None = None,

        # Distance
        distance: int | Range | None = None,

        # Rotation
        x_rotation: int | Range | None = None,
        y_rotation: int | Range | None = None,

        # Scores
        scores: dict[str, int | Range] | None = None,

        # Tag
        tag: str | None = None,

        # Team
        team: str | None = None,

        # Entity
        name: str | None = None,
        type: EntityType | str | None = None,
        predicate: Identifier | None = None,

        # Entity Data
        nbt: dict | None = None,

        # Player Data
        level: int | Range | None = None,
        gamemode: TargetSelectorSettings.TGamemode | None = None,
        advancements: dict[Identifier | Advancement, bool] | None = None,

        # Traits
        limit: int | None = None,
        sort: TargetSelectorSettings.TSort | None = None,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.dx = dx
        self.dy = dy
        self.dz = dz

        self.distance = distance

        self.x_rotation = x_rotation
        self.y_rotation = y_rotation

        self.scores = scores

        self.tag = tag

        self.team = team

        self.name = name
        self.type = type
        self.predicate = predicate

        self.nbt = nbt

        self.level = level
        self.gamemode = gamemode
        if advancements:
            adv = {}
            for k, v in advancements.items():
                id = k.id if isinstance(k, Advancement) else k
                adv[id] = v
        else:
            adv = advancements
        self.advancements = adv

        self.limit = limit
        self.sort = sort

        self.other = {}

    def _fmt_range(self, v: int | Range | None) -> int | str | None:
        if isinstance(v, Range):
            return str(v)
        return v

    def _fmt_scores(self) -> str | None:
        if not self.scores:
            return None
        return "{" + ",".join(
            f"{k}={v}" for k, v in self.scores.items()
        ) + "}"

    def to_dict(self) -> dict:
        return {
            "x": self._fmt_range(self.x),
            "y": self._fmt_range(self.y),
            "z": self._fmt_range(self.z),

            "dx": self._fmt_range(self.dx),
            "dy": self._fmt_range(self.dy),
            "dz": self._fmt_range(self.dz),

            "distance": self._fmt_range(self.distance),

            "x_rotation": self._fmt_range(self.x_rotation),
            "y_rotation": self._fmt_range(self.y_rotation),

            "scores": self._fmt_scores(),

            "tag": self.tag,

            "team": self.team,

            "name": self.name,

            "type": self.type if isinstance(self.type, str) else ~self.type.id if self.type is not None else None,

            "predicate": self.predicate,

            "nbt": SNBTSerializer.serialize(self.nbt) if self.nbt else None,

            "level": self._fmt_range(self.level),

            "gamemode": self.gamemode,

            "advancements": self.advancements,

            "limit": self.limit,
            "sort": self.sort,

            **self.other
        }
    
    def with_x(self, value: int | Range | None):
        """Sets the X coordinate."""
        self.x = value
        return self
    def with_y(self, value: int | Range | None):
        """Sets the Y coordinate."""
        self.y = value
        return self
    def with_z(self, value: int | Range | None):
        """Sets the Z coordinate."""
        self.z = value
        return self

    def with_dx(self, value: int | Range | None):
        """Sets the X volume."""
        self.dx = value
        return self
    def with_dy(self, value: int | Range | None):
        """Sets the Y volume."""
        self.dy = value
        return self
    def with_dz(self, value: int | Range | None):
        """Sets the Z volume."""
        self.dz = value
        return self

    def with_distance(self, value: int | Range | None):
        """Sets the maximum distance."""
        self.distance = value
        return self
    
    def with_x_rotation(self, value: int | Range | None):
        """Sets the X rotation (pitch)."""
        self.x_rotation = value
        return self
    def with_y_rotation(self, value: int | Range | None):
        """Sets the Y rotation (yaw)."""
        self.y_rotation = value
        return self

    def with_scores(self, value: dict[str, int | Range] | None):
        """Sets the required scores."""
        self.scores = value
        return self

    def with_tag(self, value: str | EntityTag | None):
        """Sets the entity tag."""
        self.tag = str(value)
        return self

    def with_team(self, value: str | None):
        """Sets the entity team."""
        self.team = value
        return self

    def with_name(self, value: str | None):
        """Sets the entity name."""
        self.name = value
        return self

    def with_type(self, value: EntityType | str | None):
        """Sets the entity type."""
        self.type = value
        return self

    def with_predicate(self, value: Identifier | None):
        """Sets a custom predicate."""
        self.predicate = value
        return self

    def with_nbt(self, value: dict | None):
        """Sets the entity NBT."""
        self.nbt = value
        return self

    def with_level(self, value: int | Range | None):
        """Sets the experience level."""
        self.level = value
        return self

    def with_gamemode(self, value: TargetSelectorSettings.TGamemode | None):
        """Sets the game mode."""
        self.gamemode = value
        return self

    def with_advancements(self, value: dict[Identifier | Advancement, bool] | None):
        """Sets the required advancements."""
        if value:
            adv = {}
            for k, v in value.items():
                id = k.id if isinstance(k, Advancement) else k
                adv[id] = v
        else:
            adv = value
        self.advancements = adv
        return self

    def with_limit(self, value: int | None):
        """Sets the entity limit."""
        self.limit = value
        return self

    def with_sort(self, value: TargetSelectorSettings.TSort | None):
        """Sets the result sorting order."""
        self.sort = value
        return self

    def which_holds(self, item: Item | Identifier | ItemStack):
        """Sets the item the target must be holding."""
        if isinstance(item, Identifier):
            self.nbt = { 
                "SelectedItem": { 
                    "id": item 
                } 
            }
        elif isinstance(item, Item):
            self.nbt = { 
                "SelectedItem": { 
                    "id": item.id, 
                    "components": item.settings.get_components() 
                }
            }
        elif isinstance(item, ItemStack):
            self.nbt = { 
                "SelectedItem": {
                    "id": item.item.id, 
                    "components": item.item.settings.get_components(), 
                    "count": item.count 
                } 
            }
        return self
    
    def copy(self) -> "TargetSelectorSettings":
        """Creates a copy of this TargetSelectorSettings."""
        return TargetSelectorSettings(
            x=self.x,
            y=self.y,
            z=self.z,
            dx=self.dx,
            dy=self.dy,
            dz=self.dz,
            distance=self.distance,
            x_rotation=self.x_rotation,
            y_rotation=self.y_rotation,
            scores=self.scores.copy() if self.scores else None,
            tag=self.tag,
            team=self.team,
            name=self.name,
            type=self.type,
            predicate=self.predicate,
            nbt=self.nbt.copy() if self.nbt else None,
            level=self.level,
            gamemode=self.gamemode, # type: ignore
            advancements=self.advancements.copy() if self.advancements else None,
            limit=self.limit,
            sort=self.sort # type: ignore
        )
    
    def do_first(self):
        self.with_limit(1)
        return self
    def do_nearest(self):
        self.with_sort("nearest")
        return self
    def do_furthest(self):
        self.with_sort("furthest")
        return self
    def do_rand(self):
        self.with_sort("random")
        return self
    def do_arbitrary(self):
        self.with_sort("arbitrary")
        return self
    def do_survival(self):
        self.with_gamemode("survival")
        return self
    def do_creative(self):
        self.with_gamemode("creative")
        return self
    def do_adventure(self):
        self.with_gamemode("adventure")
        return self
    def do_spectator(self):
        self.with_gamemode("spectator")
        return self
    
    def with_(self, k: str, v: Any):
        """Sets a custom key-value pair in the settings."""
        if hasattr(v, "__str__"):
            v = str(v)
        self.other[k] = v
        return self