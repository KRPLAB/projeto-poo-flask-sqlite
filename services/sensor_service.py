from models.sensor import Sensor
from database.sensor_dao import SensorDAO

class SensorService:
    def __init__(self, sensor_dao: SensorDAO = SensorDAO()):
        self.sensor_dao = sensor_dao

    def criar_sensor(self, data: dict) -> Sensor:
        sensor = Sensor(
            id = None,
            tipo = data["tipo"],
            localizacao = data.get("localizacao"),
            status = data.get("status", 'ativo'),
            dispositivo_uuid = data.get("dispositivo_uuid")
        )
        return self.sensor_dao.salvar(sensor)

    def listar_sensores(self) -> list[Sensor]:
        return self.sensor_dao.listar()

    def obter_sensor_por_id(self, sensor_id: int) -> Sensor | None:
        return self.sensor_dao.obter_sensor_por_id(sensor_id)

    def remover_sensor(self, sensor_id: int) -> bool:
        return self.sensor_dao.remover_sensor(sensor_id)

    def atualizar_sensor(self, sensor_id: int, data: dict) -> Sensor | None:
        sensor = self.obter_sensor_por_id(sensor_id)
        if sensor:
            sensor.tipo = data.get("tipo", sensor.tipo)
            sensor.localizacao = data.get("localizacao", sensor.localizacao)
            sensor.status = data.get("status", sensor.status)
            sensor.dispositivo_uuid = data.get("dispositivo_uuid", sensor.dispositivo_uuid)
            return self.sensor_dao.atualizar_sensor(sensor)
        return None