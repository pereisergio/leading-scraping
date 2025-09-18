from domain.interfaces.scrapers import IHttpClient, IWebScraper


class LojaMaetoScraper(IWebScraper):
    def __init__(self, http_client: IHttpClient) -> None:
        self._http_client = http_client
