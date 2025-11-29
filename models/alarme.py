from datetime import datetime
class Alerta:
    def __init__(self, id : int, leitura_id : int, sensor_id : int, nivel : str, mensagem : str, timestamp : datetime = None, resolvido : bool = False):
        self.id = id
        self.leitura_id = leitura_id
        self.sensor_id = sensor_id
        self.nivel = nivel
        self.mensagem = mensagem
        self.timestamp = timestamp or datetime.utcnow()
        self.resolvido = resolvido

    def enviar(self):
        pass  # Implementar lógica de envio de alerta

    def marcar_resolvido(self):
        self.resolvido = True
    
    def to_dict(self):
        return {
            "id": self.id,
            "mensagem": self.mensagem,
            "nivel": self.nivel,
            "leitura_id": self.leitura_id,
            "sensor_id": self.sensor_id,
            "timestamp": self.timestamp.isoformat() if hasattr(self.timestamp, "isoformat") else self.timestamp
        }