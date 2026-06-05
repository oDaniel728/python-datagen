class Holder[T]():
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value