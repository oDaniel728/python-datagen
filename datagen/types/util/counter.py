class Counter():
    def __init__(self) -> None:
        self._counter = 0

    def get(self) -> int:
        self._counter += 1
        return self._counter
    
    def __int__(self):
        return self.get()
    
    def __str__(self) -> str:
        return str(int(self))