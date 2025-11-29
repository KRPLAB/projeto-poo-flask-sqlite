from datetime import datetime
class Sensor:
    def __init__(self, id : int, tipo : str, localizacao : str, ativo : bool = True):
        self.id = id
        self.tipo = tipo
        self.localizacao = localizacao
        self.ativo = ativo
    
    def ativar(self):
        if not self.ativo:
            self.ativo = True
        else:
            print(f'Sensor {self.id} já está ativo.')
    
    def desativar(self):
        if self.ativo:
            self.ativo = False
        else:
            print(f'Sensor {self.id} já está desativado.')
    
    def registrar_leitura(self, valor : float, dao):
        if self.ativo:
            leitura = leitura(None, self.id, valor, datetime.utcnow())
            dao.leitura_dao.salvar(leitura)
            return leitura
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'localizacao': self.localizacao,
            'ativo': self.ativo
        }
