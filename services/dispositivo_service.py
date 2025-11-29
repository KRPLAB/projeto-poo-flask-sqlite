from models.dispositivo import Dispositivo
from database.dispositivo_dao import DispositivoDAO

dispositivo_dao = DispositivoDAO()

def criar_dispositivo(tipo: str, localizacao: str) -> Dispositivo:
    dispositivo = Dispositivo(None, tipo, localizacao)
    dispositivo_dao.salvar(dispositivo)
    return dispositivo

def listar_dispositivos() -> list[Dispositivo]:
    return dispositivo_dao.listar()

def obter_dispositivo_por_id(dispositivo_id: int) -> Dispositivo | None:
    return dispositivo_dao.obter_dispositivo_por_id(dispositivo_id)

def remover_dispositivo(dispositivo_id: int) -> bool:
    return dispositivo_dao.remover_dispositivo(dispositivo_id)

def atualizar_dispositivo(dispositivo_id: int, tipo: str, localizacao: str, ativo: bool) -> Dispositivo | None:
    dispositivo = dispositivo_dao.obter_dispositivo_por_id(dispositivo_id)
    if dispositivo:
        dispositivo.tipo = tipo
        dispositivo.localizacao = localizacao
        dispositivo.ativo = ativo
        dispositivo_dao.atualizar_dispositivo(dispositivo)
        return dispositivo
    return None