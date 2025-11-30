from datetime import datetime

class Alerta:
    def __init__(self, id: int, sensor_id: int, nivel: str, mensagem: str = None, data_hora: datetime = None, resolvido: bool = False):
        self.id = id
        self.sensor_id = sensor_id
        self.nivel = nivel
        self.mensagem = mensagem
        self.data_hora = data_hora or datetime.now()
        self.resolvido = resolvido

    def marcar_resolvido(self):
        self.resolvido = True
    
    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "nivel": self.nivel,
            "mensagem": self.mensagem,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None,
            "resolvido": self.resolvido
        }