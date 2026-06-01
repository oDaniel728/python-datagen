class Char():
    def __init__(self, char: str):
        self.char = char[0]

    def __str__(self) -> str:
        return self.char
    
    def __invert__(self) -> str:
        return self.char