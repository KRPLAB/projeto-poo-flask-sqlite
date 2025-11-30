from models.alerta import Alerta
from database.alerta_dao import AlertaDAO

class AlertaService:
    def __init__(self, alerta_dao: AlertaDAO = AlertaDAO()):
        self.alerta_dao = alerta_dao

    def criar_alerta(self, data: dict) -> Alerta:
        alerta = Alerta(
            id=None,
            sensor_id=data['sensor_id'],
            nivel=data['nivel'],
            mensagem=data.get('mensagem'),
            resolvido=data.get('resolvido', False)
        )
        return self.alerta_dao.salvar(alerta)

    def listar_alertas(self) -> list[Alerta]:
        return self.alerta_dao.listar()

    def obter_alerta_por_id(self, alerta_id: int) -> Alerta | None:
        return self.alerta_dao.obter_alerta_por_id(alerta_id)

    def remover_alerta(self, alerta_id: int) -> bool:
        return self.alerta_dao.remover_alerta(alerta_id)

    def atualizar_alerta(self, alerta_id: int, data: dict) -> Alerta | None:
        alerta = self.obter_alerta_por_id(alerta_id)
        if alerta:
            alerta.sensor_id = data.get('sensor_id', alerta.sensor_id)
            alerta.nivel = data.get('nivel', alerta.nivel)
            alerta.mensagem = data.get('mensagem', alerta.mensagem)
            alerta.resolvido = data.get('resolvido', alerta.resolvido)
            return self.alerta_dao.atualizar(alerta)
        return None