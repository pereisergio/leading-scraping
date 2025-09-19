import json
import sqlite3
from typing import TYPE_CHECKING, override

from domain.interfaces import IProductRepository

if TYPE_CHECKING:
    from domain.models import Product


# ruff: noqa: W291


class SqliteProductRepository(IProductRepository):
    def __init__(self, db_path: str = "products.db") -> None:
        self._db_path: str = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Inicializa o banco de dados e cria as tabelas necessárias."""
        with sqlite3.connect(self._db_path) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    sku TEXT PRIMARY KEY,
                    product_title TEXT NOT NULL,
                    price REAL NOT NULL,
                    price_pix REAL NOT NULL,
                    price_installments REAL NOT NULL,
                    installments_count INTEGER NOT NULL,
                    specifications TEXT NOT NULL
                )
            """)
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco de dados configurado para UTF-8."""
        conn: sqlite3.Connection = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA encoding='UTF-8'")
        return conn

    def _exists(self, sku: str) -> bool:
        """Verifica se um produto existe pelo SKU."""
        with self._get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM products WHERE sku = ?", (sku,))
            return cursor.fetchone() is not None

    def _serialize_specifications(self, specifications: dict[str, str]) -> str:
        """Serializa especificações preservando UTF-8."""
        return json.dumps(specifications, ensure_ascii=False, separators=(",", ":"))

    @override
    def create(self, product: "Product") -> None:
        """Cria um novo produto ou atualiza se já existir."""
        if self._exists(product.sku):
            self.update(product)
        else:
            self._insert_new_product(product)

    def _insert_new_product(self, product: "Product") -> None:
        """Insere um novo produto no banco de dados."""
        with self._get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO products (
                    sku, product_title, price, price_pix, 
                    price_installments, installments_count, specifications
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    product.sku,
                    product.product_title,
                    product.price,
                    product.price_pix,
                    product.price_installments,
                    product.installments_count,
                    self._serialize_specifications(product.specifications),
                ),
            )
            conn.commit()

    @override
    def update(self, product: "Product") -> None:
        """Atualiza um produto existente no banco de dados."""
        with self._get_connection() as conn:
            cursor: sqlite3.Cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE products SET 
                    product_title = ?,
                    price = ?,
                    price_pix = ?,
                    price_installments = ?,
                    installments_count = ?,
                    specifications = ?
                WHERE sku = ?
            """,
                (
                    product.product_title,
                    product.price,
                    product.price_pix,
                    product.price_installments,
                    product.installments_count,
                    self._serialize_specifications(product.specifications),
                    product.sku,
                ),
            )
            conn.commit()
