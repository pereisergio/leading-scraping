from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    product_title: str
    price: float
    price_pix: float
    price_installments: float
    installments_count: int
    specifications: dict[str, str]
