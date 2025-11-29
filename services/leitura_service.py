from models.leitura import Leitura
from database.leitura_dao import LeituraDAO
from services.sensor_service import obter_sensor_por_id

leitura_dao = LeituraDAO()

def registrar_leitura(sensor_id: int, valor: float) -> Leitura | None:
    sensor = obter_sensor_por_id(sensor_id)
    if sensor and sensor.ativo:
        leitura = Leitura(None, sensor_id, valor)
        leitura_dao.salvar(leitura)
        return leitura
    return None

def listar_leituras_por_sensor(sensor_id: int) -> list[Leitura]:
    return [l for l in leitura_dao.listar() if l.sensor_id == sensor_id]

def obter_leitura_por_id(leitura_id: int) -> Leitura | None:
    return leitura_dao.obter_leitura_por_id(leitura_id)

def remover_leitura(leitura_id: int, sensor_id: int) -> bool:
    leitura = obter_leitura_por_id(leitura_id)
    if leitura and leitura.sensor_id == sensor_id:
        return leitura_dao.remover_leitura(leitura_id)
    return False

