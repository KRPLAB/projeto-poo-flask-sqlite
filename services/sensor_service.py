from models.sensor import Sensor
from database.sensor_dao import SensorDAO

class SensorService:
    def __init__(self, sensor_dao: SensorDAO = SensorDAO()):
        self.sensor_dao = sensor_dao

    def criar_sensor(self, dispositivo_uuid: str, data: dict) -> Sensor:
        sensor = Sensor(
            id = None,
            tipo = data["tipo"],
            localizacao = data.get("localizacao"),
            status = data.get("status", 'ativo'),
            dispositivo_uuid = dispositivo_uuid
        )
        return self.sensor_dao.salvar(sensor)

    def listar_sensores(self, dispositivo_uuid: str) -> list[Sensor]:
        return self.sensor_dao.listar_por_dispositivo(dispositivo_uuid)

    def obter_sensor_por_id(self, dispositivo_uuid: str, sensor_id: int) -> Sensor | None:
        return self.sensor_dao.obter_sensor_por_id(dispositivo_uuid, sensor_id)

    def remover_sensor(self, dispositivo_uuid: str, sensor_id: int) -> bool:
        return self.sensor_dao.remover_sensor(dispositivo_uuid, sensor_id)

    def atualizar_sensor(self, dispositivo_uuid: str, sensor_id: int, data: dict) -> Sensor | None:
        sensor = self.obter_sensor_por_id(dispositivo_uuid, sensor_id)
        if sensor:
            sensor.tipo = data.get("tipo", sensor.tipo)
            sensor.localizacao = data.get("localizacao", sensor.localizacao)
            sensor.status = data.get("status", sensor.status)
            return self.sensor_dao.atualizar_sensor(sensor)
        return None