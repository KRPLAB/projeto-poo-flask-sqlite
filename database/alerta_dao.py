import sys
import os
from datetime import datetime

# adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.alerta import Alerta
from database.conexao import get_connection


class AlertaDAO:
    @staticmethod
    def criar_tabela():
        conn = get_connection()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            nivel TEXT NOT NULL,
            mensagem TEXT,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolvido INTEGER DEFAULT 0,
            FOREIGN KEY(sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(alerta: Alerta) -> Alerta:
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO alertas (sensor_id, nivel, mensagem, data_hora, resolvido) VALUES (?, ?, ?, ?, ?)",
            (alerta.sensor_id, alerta.nivel, alerta.mensagem, alerta.data_hora, int(alerta.resolvido))
        )
        alerta.id = cur.lastrowid
        conn.commit()
        conn.close()
        return alerta

    @staticmethod
    def listar() -> list[Alerta]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM alertas ORDER BY data_hora DESC")
        alertas = [
            Alerta(
                id=row['id'],
                sensor_id=row['sensor_id'],
                nivel=row['nivel'],
                mensagem=row['mensagem'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            ) for row in cur.fetchall()
        ]
        conn.close()
        return alertas
    
    @staticmethod
    def listar_por_sensor(sensor_id: int) -> list[Alerta]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM alertas WHERE sensor_id = ? ORDER BY data_hora DESC", (sensor_id,))
        alertas = [
            Alerta(
                id=row['id'],
                sensor_id=row['sensor_id'],
                nivel=row['nivel'],
                mensagem=row['mensagem'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            ) for row in cur.fetchall()
        ]
        conn.close()
        return alertas
    
    @staticmethod
    def obter_alerta_por_id(sensor_id: int, alerta_id: int) -> Alerta | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM alertas WHERE id = ? AND sensor_id = ?", (alerta_id, sensor_id))
        row = cur.fetchone()
        conn.close()
        if row:
            return Alerta(
                id=row['id'],
                sensor_id=row['sensor_id'],
                nivel=row['nivel'],
                mensagem=row['mensagem'],
                data_hora=datetime.fromisoformat(row['data_hora']) if row['data_hora'] else None,
                resolvido=bool(row['resolvido'])
            )
        return None

    @staticmethod
    def atualizar(alerta: Alerta) -> Alerta:
        conn = get_connection()
        conn.execute(
            "UPDATE alertas SET sensor_id = ?, nivel = ?, mensagem = ?, data_hora = ?, resolvido = ? WHERE id = ?",
            (alerta.sensor_id, alerta.nivel, alerta.mensagem, alerta.data_hora, int(alerta.resolvido), alerta.id)
        )
        conn.commit()
        conn.close()
        return alerta

    @staticmethod
    def remover_alerta(sensor_id: int, alerta_id: int) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM alertas WHERE id = ? AND sensor_id = ?", (alerta_id, sensor_id))
        conn.commit()
        conn.close()
        return cur.rowcount > 0