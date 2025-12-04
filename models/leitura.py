from datetime import datetime
from models.evento_sensor import EventoSensor

class Leitura(EventoSensor):
    """Representa uma leitura de sensor. Herda de EventoSensor."""
    
    def __init__(self, id: int, sensor_id: int, valor: float, data_hora: datetime = None, resolvido: bool = False):
        super().__init__(id, sensor_id, data_hora, resolvido)
        self.valor = valor

    def to_dict(self):
        """Sobrescreve to_dict para incluir o valor da leitura."""
        d = super().to_dict()
        d['valor'] = self.valor
        return d