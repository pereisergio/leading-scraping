from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    sku: str
    product_title: str
    price: float
    price_pix: float
    price_installments: float
    installments_count: int
    specifications: dict[str, str]
    url: str | None = None
    availability: bool = True
    scraped_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.scraped_at is None:
            self.scraped_at = datetime.now().astimezone()
