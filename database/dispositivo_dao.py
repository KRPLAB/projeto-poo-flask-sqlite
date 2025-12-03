import sys
import os
from uuid import uuid4

# adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.dispositivo import Dispositivo
from database.conexao import get_connection

class DispositivoDAO:
    @staticmethod
    def criar_tabela():
        conn = get_connection()
        conn.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            uuid TEXT PRIMARY KEY,
            mac_address TEXT NOT NULL UNIQUE,
            descricao TEXT,
            status TEXT DEFAULT 'offline',
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(dispositivo: Dispositivo) -> Dispositivo:
        conn = get_connection()
        conn.execute(
            "INSERT INTO dispositivos (uuid, mac_address, descricao, status, criado_em) VALUES (?, ?, ?, ?, ?)",
            (dispositivo.uuid, dispositivo.mac_address, dispositivo.descricao, dispositivo.status, dispositivo.criado_em)
        )
        conn.commit()
        conn.close()
        return dispositivo

    @staticmethod
    def listar() -> list[Dispositivo]:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM dispositivos")
        dispositivos = [Dispositivo(row['mac_address'], row['descricao'], row['status'], row['criado_em'], row['uuid']) for row in cur.fetchall()]
        conn.close()
        return dispositivos
    
    @staticmethod
    def obter_dispositivo_por_uuid(dispositivo_uuid: str) -> Dispositivo | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM dispositivos WHERE uuid = ?", (dispositivo_uuid,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Dispositivo(row['mac_address'], row['descricao'], row['status'], row['criado_em'], row['uuid'])
        return None
    
    @staticmethod
    def obter_dispositivo_por_mac(mac_address: str) -> Dispositivo | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM dispositivos WHERE mac_address = ?", (mac_address,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Dispositivo(row['mac_address'], row['descricao'], row['status'], row['criado_em'], row['uuid'])
        return None
        
    @staticmethod
    def remover_dispositivo(dispositivo_uuid: str) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM dispositivos WHERE uuid = ?", (dispositivo_uuid,))
        conn.commit()
        conn.close()
        return cur.rowcount > 0
    
    @staticmethod
    def update_dispositivo(dispositivo: Dispositivo) -> Dispositivo:
        conn = get_connection()
        conn.execute(
            "UPDATE dispositivos SET mac_address = ?, descricao = ?, status = ? WHERE uuid = ?",
            (dispositivo.mac_address, dispositivo.descricao, dispositivo.status, dispositivo.uuid)
        )
        conn.commit()
        conn.close()
        return dispositivo