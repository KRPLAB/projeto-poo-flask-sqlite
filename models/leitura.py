from datetime import datetime

class Leitura:
    def __init__(self, id: int, sensor_id: int, valor: float, data_hora: datetime = None, resolvido: bool = False):
        self.id = id
        self.sensor_id = sensor_id
        self.valor = valor
        self.data_hora = data_hora or datetime.now()
        self.resolvido = resolvido

    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'valor': self.valor,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'resolvido': self.resolvido
        }