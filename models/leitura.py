from datetime import datetime
class Leitura: 
    LIMITE_ALERTA = 1000.0
    def __init__(self, id : int, sensor_id : int, valor : float, timestamp : datetime = None):
        self.id = id
        self.sensor_id = sensor_id
        self.valor = valor
        self.timestamp = timestamp or datetime.utcnow()

    def e_alerta(self):
        return self.valor > Leitura.LIMITE_ALERTA
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'valor': self.valor,
            'timestamp': self.timestamp.isoformat()
        }