import sqlite3
from sqlite3 import Connection
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_NAME")

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn