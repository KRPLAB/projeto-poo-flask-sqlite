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

def listar_leituras() -> list[Leitura]:
    return leitura_dao.listar()

def obter_leitura_por_id(leitura_id: int) -> Leitura | None:
    return leitura_dao.obter_leitura_por_id(leitura_id)

