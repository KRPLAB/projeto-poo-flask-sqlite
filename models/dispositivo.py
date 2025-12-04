from datetime import datetime
from uuid import uuid4
from models.base_model import BaseModel


class Dispositivo(BaseModel):
    def __init__(self, mac_address: str, descricao: str = None, status: str = 'offline', criado_em: datetime = None, uuid: str = None):
        self.uuid = uuid or str(uuid4())
        self.mac_address = mac_address
        self.descricao = descricao
        self.status = status
        self.criado_em = criado_em or datetime.now()

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'mac_address': self.mac_address,
            'descricao': self.descricao,
            'status': self.status,
            'criado_em': datetime.fromisoformat(self.criado_em).isoformat() if isinstance(self.criado_em, str) else self.criado_em.isoformat() if self.criado_em else None
        }