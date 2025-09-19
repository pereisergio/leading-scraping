from dataclasses import dataclass


@dataclass
class Product:
    """
    Representa um produto coletado pelo sistema de scraping.

    Atributos:
        sku: Código identificador único do produto.
        product_title: Título ou nome do produto.
        price: Preço padrão do produto.
        price_pix: Preço do produto para pagamento via Pix.
        price_installments: Preço do produto para pagamento parcelado.
        installments_count: Número de parcelas disponíveis.
        specifications: Dicionário com especificações detalhadas do produto.
    """

    sku: str
    product_title: str
    price: float
    price_pix: float
    price_installments: float
    installments_count: int
    specifications: dict[str, str]
