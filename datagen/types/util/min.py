class Range():
    def __init__(self, min: int | None = None, max: int | None = None) -> None:
        self.start = min
        self.end = max

    @staticmethod
    def from_string(v: str) -> "Range":
        return Range(*[int(x) if x else None for x in v.split("..")])

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
    
    def __contains__(self, item: int | Range) -> bool:
        if isinstance(item, Range):
            s, e = item.start, item.end
            return (self.start is None or (s is not None and self.start <= s)) and (self.end is None or (e is not None and self.end >= e))
        else:
            return (self.start is None or self.start <= item) and (self.end is None or self.end >= item)