import requests
from domain.interfaces import IHttpClient


class RequestsHttpClient(IHttpClient):
    """
    Implementação concreta de cliente HTTP usando requests.

    Responsável por realizar requisições HTTP GET para coletar dados de páginas web.
    """

    def get(self, url: str, headers: dict[str, str] | None = None) -> str:
        """
        Realiza uma requisição HTTP GET para a URL informada.

        Args:
            url: URL de destino da requisição.
            headers: Cabeçalhos personalizados para a requisição (opcional).

        Returns:
            Conteúdo da resposta como string.
        """
        response = requests.get(url, headers=headers)  # noqa: S113
        response.raise_for_status()
        return response.text
