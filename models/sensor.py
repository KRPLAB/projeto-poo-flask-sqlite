from models.base_model import BaseModel

class Sensor(BaseModel):
    def __init__(self, id: int, tipo: str, localizacao: str = None, status: str = 'ativo', dispositivo_uuid: str = None):
        self.id = id
        self.tipo = tipo
        self.localizacao = localizacao
        self.status = status
        self.dispositivo_uuid = dispositivo_uuid

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'localizacao': self.localizacao,
            'status': self.status,
            'dispositivo_uuid': self.dispositivo_uuid
        }
