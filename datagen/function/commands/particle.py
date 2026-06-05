from datagen.function.commands.command import Command
from datagen.utils.repr.particle import ParticleType
from datagen.utils.repr.position3 import Position3


class Particle(Command):
    def __init__(self,
        type: ParticleType,
        pos: Position3,
        delta: Position3,
        speed: float,
        count: int,
        force: bool = False
    ) -> None:
        super().__init__()

        self.type = type
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.count = count
        self.force = force

    def to_string(self) -> str:
        return f"particle {self.type} {self.pos} {self.delta} {self.speed} {self.count} {'force' if self.force else 'normal'}"