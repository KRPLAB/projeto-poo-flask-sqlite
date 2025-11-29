import sys
import os

# adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.alarme import Alerta
from database.conexao import get_connection


class AlarmeDAO:
    @staticmethod
    def criar_tabela():
        conn = get_connection()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            leitura_id INTEGER NOT NULL,
            sensor_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(alarme: Alerta) -> int:
        conn = get_connection()
        cur = conn
        if alarme.id is None:
            cur = conn.execute(
                "INSERT INTO alertas (mensagem, nivel, leitura_id, sensor_id) VALUES (?, ?, ?, ?)",
                (alarme.mensagem, alarme.nivel, alarme.leitura_id, alarme.sensor_id)
            )
            alarme.id = cur.lastrowid
        else:
            conn.execute(
                "UPDATE alertas SET mensagem = ?, nivel = ?, leitura_id = ?, sensor_id = ? WHERE id = ?",
                (alarme.mensagem, alarme.nivel, alarme.leitura_id, alarme.sensor_id, alarme.id)
            )
        conn.commit()
        conn.close()
        return alarme

    @staticmethod
    def listar():
        conn = get_connection()
        if conn is None:
            return []
        
        cur = conn.execute("SELECT * FROM alertas")
        rows = cur.fetchall()
        conn.close()
        return [
            Alerta(
                id=row[0],
                mensagem=row[1],
                nivel=row[2],
                leitura_id=row[3],
                sensor_id=row[4],
                timestamp=row[5]
            ) for row in rows
        ]
    
    @staticmethod
    def obter_alerta_por_id(alarme_id: int):
        conn = get_connection()
        cur = conn.execute("SELECT * FROM alertas WHERE id = ?", (alarme_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Alerta(
                id=row[0],
                mensagem=row[1],
                nivel=row[2],
                leitura_id=row[3],
                sensor_id=row[4],
                timestamp=row[5]
            )
        return None
    @staticmethod
    def remover_alerta(alarme_id: int) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM alertas WHERE id = ?", (alarme_id,))
        conn.commit()
        conn.close()
        return cur.rowcount > 0