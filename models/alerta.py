from datetime import datetime
from models.evento_sensor import EventoSensor


class Alerta(EventoSensor):
    """Representa um evento de alerta de sensor. Herda de EventoSensor"""

    def __init__(
        self, id: int, sensor_id: int, nivel: str, mensagem: str = None, data_hora: datetime = None, resolvido: bool = False
    ):
        super().__init__(id, sensor_id, data_hora, resolvido)
        self.nivel = nivel
        self.mensagem = mensagem
        self.resolvido = resolvido

    def to_dict(self):
        """Sobrescreve to_dict para incluir nível, mensagem e status resolvido do alerta."""
        d = super().to_dict()
        d["nivel"] = self.nivel
        d["mensagem"] = self.mensagem
        d["resolvido"] = self.resolvido
        return d