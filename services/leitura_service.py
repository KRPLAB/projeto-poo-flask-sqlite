from models.leitura import Leitura
from database.leitura_dao import LeituraDAO

class LeituraService:
    def __init__(self, leitura_dao: LeituraDAO = LeituraDAO()):
        self.leitura_dao = leitura_dao

    def registrar_leitura(self, data: dict) -> Leitura:
        leitura = Leitura(
            id=None,
            sensor_id=data['sensor_id'],
            valor=data['valor'],
            resolvido=data.get('resolvido', False)
        )
        return self.leitura_dao.salvar(leitura)

    def listar_leituras(self) -> list[Leitura]:
        return self.leitura_dao.listar()

    def obter_leitura_por_id(self, leitura_id: int) -> Leitura | None:
        return self.leitura_dao.obter_leitura_por_id(leitura_id)

    def atualizar_leitura(self, leitura_id: int, data: dict) -> Leitura | None:
        leitura = self.obter_leitura_por_id(leitura_id)
        if leitura:
            leitura.sensor_id = data.get('sensor_id', leitura.sensor_id)
            leitura.valor = data.get('valor', leitura.valor)
            leitura.resolvido = data.get('resolvido', leitura.resolvido)
            return self.leitura_dao.atualizar(leitura)
        return None
