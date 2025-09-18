import re
from collections.abc import Iterator
from typing import override

from bs4 import BeautifulSoup, ResultSet, Tag
from domain.interfaces.scrapers import IHttpClient, IWebScraper
from domain.models import Product

from infrastructure.validations.exceptions import InfrastructureError


class LojaMaetoScraper(IWebScraper):
    BASE_URL: str = "https://www.lojamaeto.com/search/"

    def __init__(self, http_client: IHttpClient) -> None:
        self._http_client: IHttpClient = http_client

    def _build_search_url(self, query: str, page: int = 1) -> str:
        """Constrói a URL de busca completa."""
        return f"{self.BASE_URL}?q={query}&page={page}"

    @override
    def scrape_products(self, query: str) -> Iterator["Product"]:
        """Scraping simples e eficiente de forma síncrona."""
        page: int = 1

        while True:
            page_url: str = self._build_search_url(query, page)

            try:
                html: str = self._http_client.get(page_url)
                soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
                itens: ResultSet[Tag] = soup.select("div.item")

                if not itens:
                    break

                item: Tag
                for item in itens:
                    sku = self._extract_sku(item)
                    product_title = self._extract_product_title(item)
                    price = self._extract_price(item)
                    price_pix = self._extract_price_pix(item)
                    price_installments = self._extract_price_installments(item)
                    installments_count = self._extract_installments_count(item)
                    product_url = self._extract_product_url(item)
                    specifications: dict[str, str] = {}
                    if product_url:
                        specifications = self.scrape_product_details(product_url)
                    try:
                        if not sku or not product_title:
                            msg = "SKU ou título do produto ausente."
                            raise ValueError(msg)
                        yield Product(
                            sku=sku,
                            product_title=product_title,
                            price=price,
                            price_pix=price_pix,
                            price_installments=price_installments,
                            installments_count=installments_count,
                            specifications=specifications,
                        )
                    except (InfrastructureError, TypeError) as e:
                        error_msg: str = f"Erro ao processar item: {e}"
                        print(error_msg)
                        continue

                page += 1

            except InfrastructureError as e:
                error_msg: str = f"Erro na página {page}: {e}"
                print(error_msg)
                break

    def _extract_sku(self, item: Tag) -> str | None:
        product_div: Tag | None = item.select_one("div.product")
        return str(product_div.get("data-sku")) if product_div else None

    def _extract_product_title(self, item: Tag) -> str | None:
        title_tag: Tag | None = item.select_one("h4.product-list-name a")
        return title_tag.text.strip() if title_tag else None

    def _extract_price(self, item: Tag) -> float:
        price_tag: Tag | None = item.select_one("div.price span.to-price")
        price = price_tag.text.strip() if price_tag else None
        return self._clean_to_float(price) if price else 0.0

    def _extract_price_pix(self, item: Tag) -> float:
        price_tag: Tag | None = item.select_one(
            "div.cash-payment-container span.to-price"
        )
        price = price_tag.text.strip() if price_tag else None
        return self._clean_to_float(price) if price else 0.0

    def _extract_price_installments(self, item: Tag) -> float:
        price_tag: Tag | None = item.select_one(
            "div.product-parcel span.installments-amount"
        )
        price = price_tag.text.strip() if price_tag else None
        return self._clean_to_float(price) if price else 0.0

    def _extract_installments_count(self, item: Tag) -> int:
        qtd_parcela_tag = item.select_one("div.product-parcel span.installments-number")
        if not qtd_parcela_tag or not qtd_parcela_tag.text:
            return 0

        qtd_parcela_text: str = qtd_parcela_tag.text.strip()
        match = re.search(r"\d+", qtd_parcela_text)
        if match:
            try:
                return int(match.group())
            except (ValueError, IndexError) as e:
                print(
                    f"Erro ao converter quantidade de parcelas para int: "
                    f"'{qtd_parcela_text}' - {e}"
                )
        return 0

    def _clean_to_float(self, price_str: str) -> float:
        try:
            price = re.findall(r"\d{1,3}(?:[.,]\d{3})*[.,]\d{2}", price_str)
            return float(price[0].replace(".", "").replace(",", ".")) if price else 0.0
        except (ValueError, IndexError) as e:
            error_msg: str = f"Erro ao converter preço para float: {e}"
            print(error_msg)
            return 0.0

    def _extract_product_url(self, item: Tag) -> str | None:
        link_elem: Tag | None = item.select_one("h4.product-list-name a")
        if not link_elem or not link_elem.get("href"):
            return None

        product_url: str = str(link_elem["href"])
        if product_url.startswith("/"):
            product_url = f"https://www.lojamaeto.com{product_url}"
        return product_url

    @override
    def scrape_product_details(self, product_url: str) -> dict[str, str]:
        try:
            html: str = self._http_client.get(product_url)
            soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
            specs_table: Tag | None = soup.select_one(
                "table#product-description-table-attributes"
            )

            if not specs_table:
                return {}

            specs: dict[str, str] = {}
            rows: ResultSet[Tag] = specs_table.select("tr")

            row: Tag
            for row in rows:
                name_td: Tag | None = row.select_one("td.attribute-name")
                value_td: Tag | None = row.select_one("td.attribute-value span")

                if name_td and value_td:
                    name_text: str = name_td.get_text(strip=True)
                    value_text: str = value_td.get_text(strip=True)

                    # Só adicionar se ambos não estiverem vazios
                    if name_text and value_text:
                        specs[name_text] = value_text

            return specs

        except ValueError as e:
            error_msg: str = f"Erro ao extrair especificações de {product_url}: {e}"
            print(error_msg)
            return {}
