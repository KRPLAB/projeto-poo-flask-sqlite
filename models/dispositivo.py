class Dispositivo:
    def __init__(self, id : int, mac_address : str, descricao : str, online : bool = False):
        self.id = id
        self.mac_address = mac_address
        self.descricao = descricao
        self.online = online
    
    def conectar(self):
        if not self.online:
            self.online = True
        else:
            print(f'Dispositivo {self.id} já está conectado.')
    
    def desconectar(self):
        if self.online:
            self.online = False
        else:
            print(f'Dispositivo {self.id} já está desconectado.')
    
    def to_dict(self):
        return {
            'id': self.id,
            'mac_address': self.mac_address,
            'descricao': self.descricao,
            'online': self.online
        }
       