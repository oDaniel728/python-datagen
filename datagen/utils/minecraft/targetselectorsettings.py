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
        ...