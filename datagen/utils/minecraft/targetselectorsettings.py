from typing import Literal

from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier


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
        x: int | range | None = None,
        y: int | range | None = None,
        z: int | range | None = None,
        
        # Volume
        dx: int | range | None = None,
        dy: int | range | None = None,
        dz: int | range | None = None,

        # Distance
        distance: int | range | None = None,

        # Rotation
        x_rotation: int | range | None = None,
        y_rotation: int | range | None = None,

        # Scores
        scores: dict[str, int | range] | None = None,

        # Tag
        tag: str | None = None,

        # Team
        team: str | None = None,

        # Entity
        name: str | None = None,
        type: str | None = None,
        predicate: Identifier | None = None,

        # Entity Data
        nbt: dict | None = None,

        # Player Data
        level: int | range | None = None,
        gamemode: TargetSelectorSettings.TGamemode | None = None,
        advancements: dict[Identifier, bool] | None = None,

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
        self.advancements = advancements

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
            
            "type": self.type,
            
            "predicate": self.predicate,
            
            "nbt": self.nbt,
            
            "level": self.level,
            
            "gamemode": self.gamemode,
            
            "advancements": self.advancements,
            
            "limit": self.limit,
            "sort": self.sort
        }