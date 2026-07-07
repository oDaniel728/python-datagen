from datagen.extras.entities._util.hasproperties import HasProperties
from datagen.utils.repr.position3 import Position3


class SpawnableInRaidsEntities[T: HasProperties]:
    def with_can_join_raids(self: T, can_join_raids: bool) -> T:
        """
        Whether or not the entity can join raids.
        If true, the entity can spawn in raids and will be able to join raids if it is a villager or a villager variant.
        """
        self.properties["CanJoinRaids"] = can_join_raids
        return self
    
    def with_patrol_leader(self: T, patrol_leader: bool) -> T:
        """
        Whether or not the entity is a patrol leader.
        If true, the entity will spawn with a banner and will be able to lead patrols.
        """
        self.properties["PatrolLeader"] = patrol_leader
        return self
    
    def with_patrolling(self: T, patrolling: bool) -> T:
        """
        Whether or not the entity is patrolling.
        If true, the entity will spawn with a banner and will be able to lead patrols.
        """
        self.properties["Patrolling"] = patrolling
        return self
    
    def with_patrol_target(self: T, pos: Position3) -> T:
        """
        The position of the patrol target.
        If set, the entity will spawn with a banner and will be able to lead patrols.
        """
        self.properties["PatrolTarget"] = pos.to_list()
        return self
    
    def with_raid_id(self: T, raid_id: int) -> T:
        """
        The ID of the raid the entity is in.
        If set, the entity will spawn in a raid and will be able to join raids if it is a villager or a villager variant.
        """
        self.properties["RaidId"] = raid_id
        return self
    
    def with_wave(self: T, wave: int) -> T:
        """
        The wave of the raid the entity is in.
        If set, the entity will spawn in a raid and will be able to join raids if it is a villager or a villager variant.
        """
        self.properties["Wave"] = wave
        return self