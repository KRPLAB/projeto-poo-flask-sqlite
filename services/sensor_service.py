from models.sensor import Sensor
from database.sensor_dao import SensorDAO

sensor_dao = SensorDAO()

def criar_sensor(data: dict) -> Sensor:
    sensor = Sensor(
        id=None,
        tipo=data["tipo"],
        unidade_medida=data["unidade_medida"],
        faixa_operacao=data["faixa_operacao"],
        precisao=data["precisao"],
        fabricante=data["fabricante"],
        modelo=data["modelo"],
        ativo=data.get("ativo", True)
    )
    sensor_dao.salvar(sensor)
    return sensor

def listar_sensores() -> list[Sensor]:
    return sensor_dao.listar()

def obter_sensor_por_id(sensor_id: int) -> Sensor | None:
    return sensor_dao.obter_sensor_por_id(sensor_id)

def remover_sensor(sensor_id: int) -> bool:
    return sensor_dao.remover_sensor(sensor_id)

def atualizar_sensor(sensor_id: int, data: dict) -> Sensor | None:
    sensor = sensor_dao.obter_sensor_por_id(sensor_id)
    if sensor:
        sensor.tipo = data.get("tipo", sensor.tipo)
        sensor.unidade_medida = data.get("unidade_medida", sensor.unidade_medida)
        sensor.faixa_operacao = data.get("faixa_operacao", sensor.faixa_operacao)
        sensor.precisao = data.get("precisao", sensor.precisao)
        sensor.fabricante = data.get("fabricante", sensor.fabricante)
        sensor.modelo = data.get("modelo", sensor.modelo)
        sensor.ativo = data.get("ativo", sensor.ativo)
        sensor_dao.atualizar_sensor(sensor)
        return sensor
    return None