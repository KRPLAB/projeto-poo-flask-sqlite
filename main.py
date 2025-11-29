from database.alarme_dao import AlarmeDAO
from database.leitura_dao import LeituraDAO
from database.sensor_dao import SensorDAO

def init_db():
    AlarmeDAO.criar_tabela()
    LeituraDAO.criar_tabela()
    SensorDAO.criar_tabela()

if __name__ == "__main__":
    init_db()
