import sys
import os

# adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.leitura import Leitura
from database.conexao import get_connection

class LeituraDAO:
    @staticmethod
    def criar_tabela():
        conn = get_connection()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sensor_id) REFERENCES sensores(id)
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(leitura: Leitura) -> int:
        conn = get_connection()
        cur = conn
        if leitura.id is None:
            cur = conn.execute(
                "INSERT INTO leituras (sensor_id, valor) VALUES (?, ?)",
                (leitura.sensor_id, leitura.valor)
            )
            leitura.id = cur.lastrowid
        else:
            conn.execute(
                "UPDATE leituras SET sensor_id = ?, valor = ? WHERE id = ?",
                (leitura.sensor_id, leitura.valor, leitura.id)
            )
        conn.commit()
        conn.close()
        return leitura.id
    
    @staticmethod
    def listar() -> list[Leitura]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM leituras")
        leituras = [Leitura(row['id'], row['sensor_id'], row['valor'], row['timestamp']) for row in cur.fetchall()]
        conn.close()
        return leituras
    
    @staticmethod
    def obter_leitura_por_id(leitura_id: int) -> Leitura | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM leituras WHERE id = ?", (leitura_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Leitura(row['id'], row['sensor_id'], row['valor'], row['timestamp'])
        return None