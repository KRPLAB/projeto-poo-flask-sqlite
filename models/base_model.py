"""
Classe base para todos os modelos do sistema que fornece interface comum para serialização e manipulação de dados.
"""

from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Classe base abstrata para todos os modelos."""

    @abstractmethod
    def to_dict(self):
        """
        Converte o modelo para dicionário.
        Deve ser implementado pelas subclasses.
        """
        pass
