from typing import Literal, Self
from uuid import UUID


class AllayListener():
    def __init__(self) -> None:
        # props[event]
        self.event_s_distance: int | None = None
        self.event_s_game_event: str | None = None
        self.event_s_pos: list[float] | None = None
        self.event_s_projectile_owner: UUID | None = None
        self.event_s_source: UUID | None = None

        # props
        self.event_delay: int | None = None
        self.event_distance: int | None = None
        self.range: int | None = None
        
        # props[source]
        self.source_s_type: Literal["block", "entity"] | None = None
        self.source_s_pos: list[float] | None = None
        self.source_s_source_entity: UUID | None = None
        self.source_s_y_offset: float | None = None

    def with_event(
        self,
        distance: int | None = None,
        game_event: str | None = None,
        pos: list[float] | None = None,
        projectile_owner: UUID | None = None,
        source: UUID | None = None,
    ) -> "Self": 
        self.event_s_distance = distance
        self.event_s_game_event = game_event
        self.event_s_pos = pos
        self.event_s_projectile_owner = projectile_owner
        self.event_s_source = source
        return self
    
    def with_event_delay(self, event_delay: int) -> "Self":
        self.event_delay = event_delay
        return self
    
    def with_event_distance(self, event_distance: int) -> "Self":
        self.event_distance = event_distance
        return self
    
    def with_range(self, range: int) -> "Self":
        self.range = range
        return self
    
    def with_source_block(
        self,
        pos: list[float] | None = None,
    ) -> "Self":
        self.source_s_type = "block"
        self.source_s_pos = pos
        self.source_s_source_entity = None
        self.source_s_y_offset = None
        return self
    
    def with_source_entity(
        self,
        source_entity: UUID | None = None,
        y_offset: float | None = None,
    ) -> "Self":
        self.source_s_type = "entity"
        self.source_s_pos = None
        self.source_s_source_entity = source_entity
        self.source_s_y_offset = y_offset
        return self 
    
    def to_dict(self) -> dict:
        return {k: v for k,v in {
            "event": {
                "distance": self.event_s_distance,
                "game_event": self.event_s_game_event,
                "pos": self.event_s_pos,
                "projectile_owner": str(self.event_s_projectile_owner) if self.event_s_projectile_owner else None,
                "source": str(self.event_s_source) if self.event_s_source else None,
            },
            "event_delay": self.event_delay,
            "event_distance": self.event_distance,
            "range": self.range,
            "source": {
                "type": self.source_s_type,
                "pos": self.source_s_pos,
                "source_entity": str(self.source_s_source_entity) if self.source_s_source_entity else None,
                "y_offset": self.source_s_y_offset,
            }
        }.items() if v != None}