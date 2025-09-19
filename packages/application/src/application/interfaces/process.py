from abc import ABC, abstractmethod


class IProcessWebScrapping(ABC):
    @abstractmethod
    def process(self, search_query: str) -> None:
        pass
