from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IWebScraper(ABC):
    @abstractmethod
    def scrape_products(self, query: str) -> Iterator["Product"]:
        """
        Realiza o scraping de produtos a partir da URL informada.

        Deve retornar um iterador de objetos Product, um para cada produto
        encontrado.
        Implementações podem lidar com paginação e múltiplas requisições conforme
        necessário.
        """
        pass

    @abstractmethod
    def scrape_product_details(self, product_url: str) -> dict[str, str]:
        """
        Realiza o scraping dos detalhes de um produto específico a partir da URL
        informada.

        Deve retornar um objeto Product preenchido com todas as informações detalhadas
        do produto.
        """
        pass


class IHttpClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: dict[str, str] | None = None) -> str:
        """
        Realiza uma requisição HTTP GET para a URL informada e retorna o conteúdo da
        resposta como string.

        O parâmetro headers pode ser utilizado para enviar cabeçalhos personalizados na
        requisição.
        """
        pass
