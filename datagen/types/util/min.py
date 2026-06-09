class Range():
    def __init__(self, min: int | None = None, max: int | None = None) -> None:
        self.start = min
        self.end = max

    @staticmethod
    def min(value: int):
        return Range(value, None)
    
    @staticmethod
    def max(value: int):
        return Range(None, value)
    
    @staticmethod
    def range(min: int, max: int):
        return Range(min, max)
    
    @staticmethod
    def exact(value: int):
        return Range(value, value)

    def __str__(self) -> str:
        if self.start is not None and self.end is not None:
            return f"{self.start}..{self.end}"
        elif self.start is not None:
            return f"{self.start}.."
        elif self.end is not None:
            return f"..{self.end}"
        elif self.start == self.end:
            return f"{self.start}"
        else:
            return "-1"
    
    def to_dict(self) -> dict:
        out = {}
        if self.start is not None:
            out["min"] = self.start
        if self.end is not None:
            out["max"] = self.end
        return out