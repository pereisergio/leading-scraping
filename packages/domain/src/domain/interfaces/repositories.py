from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IProductRepository(ABC):
    @abstractmethod
    async def get_products_async(self) -> AsyncIterator["Product"]:
        pass

    @abstractmethod
    async def get_product_by_sku_async(self, sku: str) -> "Product":
        pass

    @abstractmethod
    async def create_async(self, product: "Product") -> None:
        pass

    @abstractmethod
    async def update_async(self, product: "Product") -> None:
        pass

    @abstractmethod
    async def remove_async(self, product: "Product") -> None:
        pass
