import requests
from domain.interfaces.scrapers import IHttpClient


class RequestsHttpClient(IHttpClient):
    def get(self, url: str, headers: dict[str, str] | None = None) -> str:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
