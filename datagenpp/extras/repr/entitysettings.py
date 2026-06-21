from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.minecraft.text._components import LiteralText
from datagen.types.util.reprs import *

class EntitySettings():
    def __init__(self) -> None:
        self.nbt = {}

    def with_nbt(self, nbt: compound):
        self.nbt.update(nbt)
        return self

    def with_settings(self, settings: EntitySettings):
        self.nbt.update(settings.to_dict())
        return self

    def to_dict(self) -> dict:
        return self.nbt
    
    def with_air(self, value: short):
        self.nbt['Air'] = value
        return self
    
    def with_custom_name(self, value: str | BaseText | list[BaseText]):
        if isinstance(value, str):
            value = f'"{value}"'
            self.nbt['CustomName'] = value

        elif isinstance(value, list):
            self.nbt['CustomName'] = [v.to_dict() for v in value]
        
        else:
            self.nbt['CustomName'] = value.to_dict()
        return self
    
    def with_custom_name_visible(self, value: boolean):
        self.nbt['CustomNameVisible'] = int(value)
        return self
    
    def with_data(self, value: compound):
        self.nbt['data'] = value
        return self
    
    def with_fall_distance(self, value: double):
        self.nbt['fall_distance'] = value
        return self
    
    def with_fire(self, value: short):
        self.nbt['Fire'] = value
        return self
    
    def with_glowing(self, value: boolean):
        self.nbt['Glowing'] = int(value)
        return self
    
    def with_visual_fire(self, value: boolean):
        self.nbt['HasVisualFire'] = int(value)
        return self
    
    def with_id(self, id: Identifier):
        self.nbt['id'] = id.to_string()
        return self
    
    def with_invulnerable(self, value: boolean):
        self.nbt['Invulnerable'] = int(value)
        return self
    
    def with_motion(self, value: tuple3[double]):
        if len(value) != 3:
            raise ValueError("Motion must be a tuple of 3 doubles (x, y, z)")
        self.nbt['Motion'] = list(value)
        return self
    
    def with_no_gravity(self, value: boolean):
        self.nbt['NoGravity'] = int(value)
        return self
    
    def with_on_ground(self, value: boolean):
        self.nbt['OnGround'] = int(value)
        return self
    
    def with_passengers(self, passengers: array[EntitySettings]):
        arr = []
        for passenger in passengers:
            if passenger == self:
                raise ValueError("An entity cannot be a passenger of itself")
            elif not isinstance(passenger, EntitySettings):
                raise ValueError("Passengers must be a list of EntitySettings")
            arr.append(passenger.to_dict())
        self.nbt['Passengers'] = arr
        return self
    
    def with_portal_cooldown(self, value: short):
        self.nbt['PortalCooldown'] = value
        return self
    
    def with_rotation(self, value: tuple2[float]):
        if len(value) != 2:
            raise ValueError("Rotation must be a tuple of 2 floats (x, y)")
        self.nbt['Rotation'] = list(value)
        return self
    
    def with_position(self, value: tuple3[double]):
        if len(value) != 3:
            raise ValueError("Position must be a tuple of 3 doubles (x, y, z)")
        self.nbt['Pos'] = list(value)
        return self
    
    def with_silent(self, value: boolean):
        self.nbt['Silent'] = int(value)
        return self
    
    def with_tags(self, tags: array[str]):
        self.nbt['Tags'] = tags
        return self
    
    def with_ticks_frozen(self, value: int):
        self.nbt['TicksFrozen'] = value
        return self