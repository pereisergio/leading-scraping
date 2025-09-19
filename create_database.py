import sqlite3


def create_database(db_path: str = "products.db") -> None:
    """Cria o banco de dados e a tabela products."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
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


if __name__ == "__main__":
    create_database()
