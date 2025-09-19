from abc import ABC, abstractmethod


class IProcessWebScrapping(ABC):
    """
    Interface para o processo de web scraping na camada de aplicação.

    Define o método process, responsável por orquestrar a busca de produtos
    conforme o termo informado.
    """

    @abstractmethod
    def process(self, search_query: str) -> None:
        """
        Executa o processo de scraping para o termo de busca informado.

        Args:
            search_query: Termo de busca para coletar produtos.
        """
        pass
