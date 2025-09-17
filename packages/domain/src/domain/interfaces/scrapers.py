from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IWebScraper(ABC):
    @abstractmethod
    async def scrape_products_async(self, url: str) -> AsyncIterator["Product"]:
        """Scrape products from a given URL"""
        pass

    @abstractmethod
    async def scrape_product_details_async(self, product_url: str) -> "Product":
        """Scrape detailed product information from product page"""
        pass


class IHttpClient(ABC):
    @abstractmethod
    async def get_async(self, url: str, headers: dict[str, str] | None = None) -> str:
        """Make HTTP GET request and return response content"""
        pass
