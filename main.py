import sys

from domain.models import Product
from infrastructure.scrapper.http_client import RequestsHttpClient
from infrastructure.scrapper.maeto_scrapper import LojaMaetoScraper


def main() -> None:
    """Função principal da aplicação de scraping."""

    # Configuração
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
    else:
        return

    # Inicialização do scraper
    http_client: RequestsHttpClient = RequestsHttpClient()
    scraper: LojaMaetoScraper = LojaMaetoScraper(http_client)

    print(f"🔍 Iniciando scraping para: '{search_query}'")
    print("=" * 70)

    try:
        product_count: int = 0

        # Agora passamos apenas o termo de busca
        product: Product
        for product in scraper.scrape_products(search_query):
            product_count += 1

            print(f"📦 Produto #{product_count}")
            print(f"   SKU: {product.sku}")
            print(f"   Nome: {product.product_title}")
            print(f"   Preço: R$ {product.price:.2f}")
            print(f"   Preço PIX: R$ {product.price_pix:.2f}")
            print(
                f"   Parcelado: {product.installments_count}x de R$ {product.price_installments:.2f}"
            )
            print(f"   📋 Especificações: {product.specifications}")

            print("-" * 70)

            # Limitar para demonstração
            if product_count >= 10:
                break

        print(f"✅ Total de produtos processados: {product_count}")

    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
