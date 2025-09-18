from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IProductRepository(ABC):
    @abstractmethod
    def create_async(self, product: "Product") -> None:
        pass

    @abstractmethod
    def update_async(self, product: "Product") -> None:
        pass
