from models.alarme import Alerta
from database.alarme_dao import AlarmeDAO

alarme_dao = AlarmeDAO()

def criar_alerta(data: dict) -> Alerta:
    alerta = Alerta(
        id=None,
        nivel_severidade=data["nivel_severidade"],
        mensagem=data["mensagem"],
        ativo=data.get("ativo", True)
    )
    alarme_dao.salvar(alerta)
    return alerta

def listar_alertas() -> list[Alerta]:
    return alarme_dao.listar()

def obter_alerta_por_id(alerta_id: int) -> Alerta | None:
    return alarme_dao.obter_alerta_por_id(alerta_id)

def remover_alerta(alerta_id: int) -> bool:
    return alarme_dao.remover_alerta(alerta_id)