import sys
from typing import TYPE_CHECKING

from application.services import ProcessScrappingService
from domain.validations.exceptions import DomainValidationError
from infrastructure.repositories import SqliteProductRepository
from infrastructure.scrapper import LojaMaetoScraper, RequestsHttpClient
from infrastructure.validations.exceptions import InfrastructureError

if TYPE_CHECKING:
    from application.interfaces import IProcessWebScrapping
    from domain.interfaces import IHttpClient, IProductRepository, IWebScraper

VERDE = "\033[32m"
AMARELO = "\033[33m"
VERMELHO = "\033[31m"
RESET = "\033[0m"
CINZA = "\033[2m"


def main() -> None:
    """Função principal usando camada de aplicação."""

    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        search_query: str = sys.argv[1]
    else:
        print(f"{VERMELHO}Erro de uso: python main.py <termo_de_busca>{RESET}")
        print(f"{CINZA}   Exemplo: python main.py casa{RESET}")
        return

    print(f"{VERDE}Iniciando scraping da consulta: '{search_query}'{RESET}")
    print("=" * 70)

    try:
        # Inicialização das dependências (camada de infraestrutura)
        http_client: IHttpClient = RequestsHttpClient()
        scraper: IWebScraper = LojaMaetoScraper(http_client)
        repository: IProductRepository = SqliteProductRepository("products.db")

        # Inicialização do serviço da camada de aplicação
        scraping_service: IProcessWebScrapping = ProcessScrappingService(
            repository=repository, scrapper=scraper
        )

        # Executar o processo de scraping
        scraping_service.process(search_query)

        print("=" * 70)
        print(f"{VERDE}Scraping concluído com sucesso!{RESET}")

    except KeyboardInterrupt:
        print(f"\n{AMARELO}  Scraping interrompido pelo usuário{RESET}")

    except (InfrastructureError, DomainValidationError) as error:
        print(f"{VERMELHO}Erro durante o scraping: {error}{RESET}")


if __name__ == "__main__":
    main()
