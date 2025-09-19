from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IWebScraper(ABC):
    """
    Interface para scrapers de produtos.

    Define métodos para coletar produtos e detalhes de produtos a partir de
    fontes externas.
    """

    @abstractmethod
    def scrape_products(self, query: str) -> Iterator["Product"]:
        """
        Coleta produtos de acordo com o termo de busca informado.

        Args:
            query: Termo de busca para filtrar produtos.

        Returns:
            Iterator de objetos Product encontrados.
        """
        pass

    @abstractmethod
    def scrape_product_details(self, product_url: str) -> dict[str, str]:
        """
        Coleta os detalhes de um produto específico a partir da URL informada.

        Args:
            product_url: URL do produto a ser detalhado.

        Returns:
            Dicionário com informações detalhadas do produto.
        """
        pass


class IHttpClient(ABC):
    """
    Interface para clientes HTTP.

    Define método para realizar requisições HTTP GET e retornar o conteúdo da resposta.
    """

    @abstractmethod
    def get(self, url: str, headers: dict[str, str] | None = None) -> str:
        """
        Realiza uma requisição HTTP GET para a URL informada.

        Args:
            url: URL de destino da requisição.
            headers: Cabeçalhos personalizados para a requisição (opcional).

        Returns:
            Conteúdo da resposta como string.
        """
        pass
