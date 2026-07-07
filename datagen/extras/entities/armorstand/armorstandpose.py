from datagen.types.util.reprs import tuple3 as _tuple3

type tuple3[T] = _tuple3[T] | list[T]
class ArmorStandPose():
    def __init__(
        self,
        body: tuple3[float] = (0.0, 0.0, 0.0),
        head: tuple3[float] = (0.0, 0.0, 0.0),
        leftarm: tuple3[float] = (0.0, 0.0, 0.0),
        leftleg: tuple3[float] = (0.0, 0.0, 0.0),
        rightarm: tuple3[float] = (0.0, 0.0, 0.0),
        rightleg: tuple3[float] = (0.0, 0.0, 0.0)
    ) -> None:
        self.body: tuple3[float] = body
        self.head: tuple3[float] = head
        self.leftarm: tuple3[float] = leftarm
        self.leftleg: tuple3[float] = leftleg
        self.rightarm: tuple3[float] = rightarm
        self.rightleg: tuple3[float] = rightleg

    def with_body(self, body: tuple3[float]) -> "ArmorStandPose":
        self.body = body
        return self
    
    def with_head(self, head: tuple3[float]) -> "ArmorStandPose":
        self.head = head
        return self
    
    def with_leftarm(self, leftarm: tuple3[float]) -> "ArmorStandPose":
        self.leftarm = leftarm
        return self
    
    def with_leftleg(self, leftleg: tuple3[float]) -> "ArmorStandPose":
        self.leftleg = leftleg
        return self
    
    def with_rightarm(self, rightarm: tuple3[float]) -> "ArmorStandPose":
        self.rightarm = rightarm
        return self
    
    def with_rightleg(self, rightleg: tuple3[float]) -> "ArmorStandPose":
        self.rightleg = rightleg
        return self
    
    def to_dict(self) -> dict:
        return {
            k: v for k, v in
            {
                "Body": self.body,
                "Head": self.head,
                "LeftArm": self.leftarm,
                "LeftLeg": self.leftleg,
                "RightArm": self.rightarm,
                "RightLeg": self.rightleg
            }.items() if len(v) == 3 and tuple(v) != (0.0, 0.0, 0.0)
        }