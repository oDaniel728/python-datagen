from abc import ABC, abstractmethod


class ValidPredicate(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()