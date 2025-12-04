"""
Classe base para todos os modelos do sistema que fornece interface comum para serialização e manipulação de dados.
"""

class BaseModel:
    """Classe base abstrata para todos os modelos."""
    
    def to_dict(self):
        """
        Converte o modelo para dicionário.
        Deve ser implementado pelas subclasses.
        """
        pass
