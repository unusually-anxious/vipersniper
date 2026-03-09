from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_event: dict) -> list[dict]:
        raise NotImplementedError
