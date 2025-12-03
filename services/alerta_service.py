from models.alerta import Alerta
from database.alerta_dao import AlertaDAO

class AlertaService:
    def __init__(self, alerta_dao: AlertaDAO = AlertaDAO()):
        self.alerta_dao = alerta_dao

    def criar_alerta(self, dispositivo_uuid: str, sensor_id: int, data: dict) -> Alerta:
        alerta = Alerta(
            id=None,
            sensor_id=sensor_id,
            nivel=data['nivel'],
            mensagem=data.get('mensagem'),
            resolvido=data.get('resolvido', False)
        )
        return self.alerta_dao.salvar(alerta)

    def listar_alertas(self, dispositivo_uuid: str, sensor_id: int) -> list[Alerta]:
        return self.alerta_dao.listar_por_sensor(sensor_id)

    def obter_alerta_por_id(self, dispositivo_uuid: str, sensor_id: int, alerta_id: int) -> Alerta | None:
        return self.alerta_dao.obter_alerta_por_id(sensor_id, alerta_id)

    def remover_alerta(self, dispositivo_uuid: str, sensor_id: int, alerta_id: int) -> bool:
        return self.alerta_dao.remover_alerta(sensor_id, alerta_id)