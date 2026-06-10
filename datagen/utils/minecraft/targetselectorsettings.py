from typing import Literal

from datagen.advancement.advancement import Advancement
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.entitytype import EntityType


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

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,

            "dx": self.dx,
            "dy": self.dy,
            "dz": self.dz,

            "distance": self.distance,

            "x_rotation": self.x_rotation,
            "y_rotation": self.y_rotation,
            
            "scores": self.scores,
            
            "tag": self.tag,
            
            "team": self.team,
            
            "name": self.name,
            
            "type": self.type if isinstance(self.type, str) else ~self.type.id if self.type is not None else None,
            
            "predicate": self.predicate,
            
            "nbt": self.nbt,
            
            "level": self.level,
            
            "gamemode": self.gamemode,
            
            "advancements": self.advancements,
            
            "limit": self.limit,
            "sort": self.sort
        }