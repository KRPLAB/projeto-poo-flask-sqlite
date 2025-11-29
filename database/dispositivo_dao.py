import sys
import os

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo TEXT,
            fabricante TEXT,
            ativo INTEGER NOT NULL DEFAULT 1
        )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def salvar(dispositivo: Dispositivo) -> int:
        conn = get_connection()
        cur = conn
        if dispositivo.id is None:
            cur = conn.execute(
                "INSERT INTO dispositivos (nome, modelo, fabricante, ativo) VALUES (?, ?, ?, ?)",
                (dispositivo.nome, dispositivo.modelo, dispositivo.fabricante, int(dispositivo.ativo))
            )
            dispositivo.id = cur.lastrowid
        else:
            conn.execute(
                "UPDATE dispositivos SET nome = ?, modelo = ?, fabricante = ?, ativo = ? WHERE id = ?",
                (dispositivo.nome, dispositivo.modelo, dispositivo.fabricante, int(dispositivo.ativo), dispositivo.id)
            )
        conn.commit()
        conn.close()
        return dispositivo

    @staticmethod
    def listar() -> list[Dispositivo]:
            conn = get_connection()
            cur = conn.execute("SELECT * FROM dispositivos")
            dispositivos = [Dispositivo(row['id'], row['nome'], row['modelo'], row['fabricante'], bool(
                row['ativo'])) for row in cur.fetchall()]
            conn.close()
            return dispositivos
    
    @staticmethod
    def obter_dispositivo_por_id(dispositivo_id: int) -> Dispositivo | None:
        conn = get_connection()
        cur = conn.execute("SELECT * FROM dispositivos WHERE id = ?", (dispositivo_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Dispositivo(row['id'], row['nome'], row['modelo'], row['fabricante'], bool(row['ativo']))
        
    @staticmethod
    def remover_dispositivo(dispositivo_id: int) -> bool:
        conn = get_connection()
        cur = conn.execute("DELETE FROM dispositivos WHERE id = ?", (dispositivo_id,))
        conn.commit()
        conn.close()
        return cur.rowcount > 0
    
    @staticmethod
    def update_dispositivo(dispositivo: Dispositivo) -> Dispositivo:
        conn = get_connection()
        conn.execute(
            "UPDATE dispositivos SET nome = ?, modelo = ?, fabricante = ?, ativo = ? WHERE id = ?",
            (dispositivo.nome, dispositivo.modelo, dispositivo.fabricante, int(dispositivo.ativo), dispositivo.id)
        )
        conn.commit()
        conn.close()
        return dispositivo