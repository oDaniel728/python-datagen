from datagen.extras.repr.entity import Entity
from datagen.extras.repr.entitysettings import EntitySettings
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.repr.entitytype import EntityType
from datagen.types.util.reprs import *

class MobEntity(Entity):
    def __init__(self, type: EntityType):
        super().__init__(type, {})

    def to_dict(self) -> dict:
        return self.properties | {"id": self.type.id}

    def with_air(self, value: short):
        self.properties['Air'] = value
        return self
    
    def with_custom_name(self, value: str | BaseText | list[BaseText]):
        if isinstance(value, str):
            value = f'"{value}"'
            self.properties['CustomName'] = value

        elif isinstance(value, list):
            self.properties['CustomName'] = [v.to_dict() for v in value]
        
        else:
            self.properties['CustomName'] = value.to_dict()
        return self
    
    def with_custom_name_visible(self, value: boolean):
        self.properties['CustomNameVisible'] = int(value)
        return self
    
    def with_data(self, value: compound):
        self.properties['data'] = value
        return self
    
    def with_fall_distance(self, value: double):
        self.properties['fall_distance'] = value
        return self
    
    def with_fire(self, value: short):
        self.properties['Fire'] = value
        return self
    
    def with_glowing(self, value: boolean):
        self.properties['Glowing'] = int(value)
        return self
    
    def with_visual_fire(self, value: boolean):
        self.properties['HasVisualFire'] = int(value)
        return self
    
    def with_id(self, id: Identifier):
        self.properties['id'] = id.to_string()
        return self
    
    def with_invulnerable(self, value: boolean):
        self.properties['Invulnerable'] = int(value)
        return self
    
    def with_motion(self, value: tuple3[double]):
        if len(value) != 3:
            raise ValueError("Motion must be a tuple of 3 doubles (x, y, z)")
        self.properties['Motion'] = list(value)
        return self
    
    def with_no_gravity(self, value: boolean):
        self.properties['NoGravity'] = int(value)
        return self
    
    def with_on_ground(self, value: boolean):
        self.properties['OnGround'] = int(value)
        return self
    
    def with_passengers(self, passengers: array[EntitySettings | Entity]):
        arr = []
        for passenger in passengers:
            if isinstance(passenger, EntitySettings):
                arr.append(passenger.to_dict())
            elif isinstance(passenger, Entity):
                arr.append(passenger.nbt())
            else:
                raise ValueError("Passenger must be an instance of EntitySettings or Entity")
        self.properties['Passengers'] = arr
        return self
    
    def with_portal_cooldown(self, value: short):
        self.properties['PortalCooldown'] = value
        return self
    
    def with_rotation(self, value: tuple2[float]):
        if len(value) != 2:
            raise ValueError("Rotation must be a tuple of 2 floats (x, y)")
        self.properties['Rotation'] = list(value)
        return self
    
    def with_position(self, value: tuple3[double]):
        if len(value) != 3:
            raise ValueError("Position must be a tuple of 3 doubles (x, y, z)")
        self.properties['Pos'] = list(value)
        return self
    
    def with_silent(self, value: boolean):
        self.properties['Silent'] = int(value)
        return self
    
    def with_tags(self, tags: array[str]):
        self.properties['Tags'] = tags
        return self
    
    def with_ticks_frozen(self, value: int):
        self.properties['TicksFrozen'] = value
        return self