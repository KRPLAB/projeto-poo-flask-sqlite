"""
Classe base para eventos de sensores (Leitura e Alerta).
Demonstra herança e polimorfismo em POO.
"""
from datetime import datetime
from models.base_model import BaseModel


class EventoSensor(BaseModel):
    """
    Classe base para eventos relacionados a sensores.
    Contém atributos comuns a Leitura e Alerta.
    """
    
    def __init__(self, id: int, sensor_id: int, data_hora: datetime = None, resolvido: bool = False):
        self.id = id
        self.sensor_id = sensor_id
        self.data_hora = data_hora or datetime.now()
        self.resolvido = resolvido
    
    def to_dict(self):
        """Serializa atributos comuns a todos os eventos."""
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'data_hora': self.data_hora.isoformat() if isinstance(self.data_hora, datetime) else self.data_hora,
            'resolvido': self.resolvido
        }
    
    def marcar_resolvido(self):
        """Marca o evento como resolvido."""
        self.resolvido = True
