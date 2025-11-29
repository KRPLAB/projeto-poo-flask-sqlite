from models.alarme import Alerta
from database.alarme_dao import AlarmeDAO

alarme_dao = AlarmeDAO()

def criar_alerta(sensor_id: int, data: dict) -> Alerta:
    alerta = Alerta(
        id=None,
        sensor_id=sensor_id,
        nivel_severidade=data["nivel_severidade"],
        mensagem=data["mensagem"],
        ativo=data.get("ativo", True)
    )
    alarme_dao.salvar(alerta)
    return alerta

def listar_alertas_por_sensor(sensor_id: int) -> list[Alerta]:
    return [a for a in alarme_dao.listar() if a.sensor_id == sensor_id]

def obter_alerta_por_id(alerta_id: int) -> Alerta | None:
    return alarme_dao.obter_alerta_por_id(alerta_id)

def remover_alerta(alerta_id: int, sensor_id: int) -> bool:
    alerta = obter_alerta_por_id(alerta_id)
    if alerta and alerta.sensor_id == sensor_id:
        return alarme_dao.remover_alerta(alerta_id)
    return False