import sys
import os
from datetime import datetime

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
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolvido INTEGER DEFAULT 0,
            FOREIGN KEY(sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(leitura: Leitura) -> Leitura:
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO leituras (sensor_id, valor, data_hora, resolvido) VALUES (?, ?, ?, ?)",
            (leitura.sensor_id, leitura.valor, leitura.data_hora, int(leitura.resolvido))
        )
        leitura.id = cur.lastrowid
        conn.commit()
        conn.close()
        return leitura
    
    @staticmethod
    def listar() -> list[Leitura]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM leituras ORDER BY data_hora DESC")
        leituras = [
            Leitura(
                id=row['id'],
                sensor_id=row['sensor_id'],
                valor=row['valor'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            ) for row in cur.fetchall()
        ]
        conn.close()
        return leituras
    
    @staticmethod
    def listar_por_sensor(sensor_id: int) -> list[Leitura]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM leituras WHERE sensor_id = ? ORDER BY data_hora DESC", (sensor_id,))
        leituras = [
            Leitura(
                id=row['id'],
                sensor_id=row['sensor_id'],
                valor=row['valor'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            ) for row in cur.fetchall()
        ]
        conn.close()
        return leituras
    
    @staticmethod
    def obter_leitura_por_id(sensor_id: int, leitura_id: int) -> Leitura | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM leituras WHERE id = ? AND sensor_id = ?", (leitura_id, sensor_id))
        row = cur.fetchone()
        conn.close()
        if row:
            return Leitura(
                id=row['id'],
                sensor_id=row['sensor_id'],
                valor=row['valor'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            )
        return None

    @staticmethod
    def remover_leitura(sensor_id: int, leitura_id: int) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM leituras WHERE id = ? AND sensor_id = ?", (leitura_id, sensor_id))
        conn.commit()
        conn.close()
        return cur.rowcount > 0