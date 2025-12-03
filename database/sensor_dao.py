import sys
import os

# adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.sensor import Sensor
from database.conexao import get_connection


class SensorDAO:
    @staticmethod
    def criar_tabela():
        conn = get_connection()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            localizacao TEXT,
            status TEXT DEFAULT 'ativo',
            dispositivo_uuid TEXT,
            FOREIGN KEY(dispositivo_uuid) REFERENCES dispositivos(uuid)
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(sensor: Sensor) -> Sensor:
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO sensores (tipo, localizacao, status, dispositivo_uuid) VALUES (?, ?, ?, ?)",
            (sensor.tipo, sensor.localizacao, sensor.status, sensor.dispositivo_uuid)
        )
        sensor.id = cur.lastrowid
        conn.commit()
        conn.close()
        return sensor

    @staticmethod
    def listar() -> list[Sensor]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM sensores")
        sensores = [Sensor(row['id'], row['tipo'], row['localizacao'], row['status'], row['dispositivo_uuid']) for row in cur.fetchall()]
        conn.close()
        return sensores
    
    @staticmethod
    def listar_por_dispositivo(dispositivo_uuid: str) -> list[Sensor]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM sensores WHERE dispositivo_uuid = ?", (dispositivo_uuid,))
        sensores = [Sensor(row['id'], row['tipo'], row['localizacao'], row['status'], row['dispositivo_uuid']) for row in cur.fetchall()]
        conn.close()
        return sensores
    
    @staticmethod
    def obter_sensor_por_id(dispositivo_uuid: str, sensor_id: int) -> Sensor | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM sensores WHERE id = ? AND dispositivo_uuid = ?", (sensor_id, dispositivo_uuid))
        row = cur.fetchone()
        conn.close()
        if row:
            return Sensor(row['id'], row['tipo'], row['localizacao'], row['status'], row['dispositivo_uuid'])
        return None

    @staticmethod
    def remover_sensor(dispositivo_uuid: str, sensor_id: int) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM sensores WHERE id = ? AND dispositivo_uuid = ?", (sensor_id, dispositivo_uuid))
        conn.commit()
        conn.close()
        return cur.rowcount > 0
    
    @staticmethod
    def atualizar_sensor(sensor: Sensor) -> Sensor:
        conn = get_connection()
        conn.execute(
            "UPDATE sensores SET tipo = ?, localizacao = ?, status = ?, dispositivo_uuid = ? WHERE id = ?",
            (sensor.tipo, sensor.localizacao, sensor.status, sensor.dispositivo_uuid, sensor.id)
        )
        conn.commit()
        conn.close()
        return sensor