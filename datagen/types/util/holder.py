class Holder[T]():
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)