from typing import TYPE_CHECKING

from application.interfaces import IProcessWebScrapping

if TYPE_CHECKING:
    from domain.interfaces import IProductRepository, IWebScraper


class ProcessScrappingService(IProcessWebScrapping):
    def __init__(
        self, repository: "IProductRepository", scrapper: "IWebScraper"
    ) -> None:
        self._repository = repository
        self._scrapper = scrapper

    def process(self, search_query: str) -> None:
        for product in self._scrapper.scrape_products(search_query):
            print(f"Processando produto: {product.product_title} (SKU: {product.sku})")
            self._repository.create(product)
