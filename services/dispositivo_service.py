from models.dispositivo import Dispositivo
from database.dispositivo_dao import DispositivoDAO

class DispositivoService:
    def __init__(self, dispositivo_dao: DispositivoDAO = DispositivoDAO()):
        self.dispositivo_dao = dispositivo_dao

    def criar_dispositivo(self, data: dict) -> Dispositivo:
        dispositivo = Dispositivo(
            mac_address=data['mac_address'],
            descricao=data.get('descricao')
        )
        return self.dispositivo_dao.salvar(dispositivo)

    def listar_dispositivos(self) -> list[Dispositivo]:
        return self.dispositivo_dao.listar()

    def obter_dispositivo_por_uuid(self, dispositivo_uuid: str) -> Dispositivo | None:
        return self.dispositivo_dao.obter_dispositivo_por_uuid(dispositivo_uuid)

    def remover_dispositivo(self, dispositivo_uuid: str) -> bool:
        return self.dispositivo_dao.remover_dispositivo(dispositivo_uuid)

    def atualizar_dispositivo(self, dispositivo_uuid: str, data: dict) -> Dispositivo | None:
        dispositivo = self.obter_dispositivo_por_uuid(dispositivo_uuid)
        if dispositivo:
            dispositivo.mac_address = data.get('mac_address', dispositivo.mac_address)
            dispositivo.descricao = data.get('descricao', dispositivo.descricao)
            dispositivo.status = data.get('status', dispositivo.status)
            return self.dispositivo_dao.update_dispositivo(dispositivo)
        return None