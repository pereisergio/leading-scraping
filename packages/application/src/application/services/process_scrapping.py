from typing import TYPE_CHECKING

from application.interfaces import IProcessWebScrapping

if TYPE_CHECKING:
    from domain.interfaces import IProductRepository, IWebScraper


class ProcessScrappingService(IProcessWebScrapping):
    """
    Serviço responsável por orquestrar o processo de scraping de produtos.

    Utiliza um repositório para persistência e um scraper para coleta dos produtos.
    """

    def __init__(
        self, repository: "IProductRepository", scrapper: "IWebScraper"
    ) -> None:
        """
        Inicializa o serviço de scraping.

        Args:
            repository: Instância que implementa IProductRepository para persistência.
            scrapper: Instância que implementa IWebScraper para coleta dos produtos.
        """
        self._repository = repository
        self._scrapper = scrapper

    def process(self, search_query: str) -> None:
        """
        Executa o processo de scraping para o termo de busca informado.

        Args:
            search_query: Termo de busca para coletar produtos.
        """
        for product in self._scrapper.scrape_products(search_query):
            print(f"Processando produto: {product.product_title} (SKU: {product.sku})")
            self._repository.create(product)
