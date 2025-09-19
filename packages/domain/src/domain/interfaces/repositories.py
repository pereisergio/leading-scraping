from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models import Product


class IProductRepository(ABC):
    """
    Interface para repositórios de produtos.

    Define métodos para criar e atualizar objetos Product na camada de persistência.
    """

    @abstractmethod
    def create(self, product: "Product") -> None:
        """
        Persiste um novo produto no repositório.

        Args:
            product: Instância de Product a ser criada.
        """
        pass

    @abstractmethod
    def update(self, product: "Product") -> None:
        """
        Atualiza os dados de um produto existente no repositório.

        Args:
            product: Instância de Product com dados atualizados.
        """
        pass
