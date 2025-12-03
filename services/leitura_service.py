from models.leitura import Leitura
from database.leitura_dao import LeituraDAO

class LeituraService:
    def __init__(self, leitura_dao: LeituraDAO = LeituraDAO()):
        self.leitura_dao = leitura_dao

    def registrar_leitura(self, dispositivo_uuid: str, sensor_id: int, data: dict) -> Leitura:
        leitura = Leitura(
            id=None,
            sensor_id=sensor_id,
            valor=data['valor'],
            resolvido=data.get('resolvido', False)
        )
        return self.leitura_dao.salvar(leitura)

    def listar_leituras(self, dispositivo_uuid: str, sensor_id: int) -> list[Leitura]:
        return self.leitura_dao.listar_por_sensor(sensor_id)

    def obter_leitura_por_id(self, dispositivo_uuid: str, sensor_id: int, leitura_id: int) -> Leitura | None:
        return self.leitura_dao.obter_leitura_por_id(sensor_id, leitura_id)

    def remover_leitura(self, dispositivo_uuid: str, sensor_id: int, leitura_id: int) -> bool:
        return self.leitura_dao.remover_leitura(sensor_id, leitura_id)
