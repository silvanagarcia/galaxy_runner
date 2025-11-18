

### Sistema de base de datos SQLite para puntuaciones


import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, db_name: str = "galaxy_runner.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        
        ### Obtener conexión a la base de datos

        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        
        ### Inicializar tablas de la base de datos
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de jugadores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de puntuaciones

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_player(self, name: str) -> int:
        
        ### Agregar un nuevo jugador y retornar su ID
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
        player_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return player_id
    
    def add_score(self, player_id: int, score: int, level: int):
        
        ### Agregar una puntuación

        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO scores (player_id, score, level) VALUES (?, ?, ?)",
            (player_id, score, level)
        )
        
        conn.commit()
        conn.close()
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, int]]:
        
        ### Obtener top puntuaciones con nombres de jugadores
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.name, s.score, s.level
            FROM scores s
            JOIN players p ON s.player_id = p.id
            ORDER BY s.score DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_player_scores(self, player_id: int) -> List[Tuple[int, int]]:
        
        ### Obtener todas las puntuaciones de un jugador

        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT score, level FROM scores WHERE player_id = ? ORDER BY score DESC",
            (player_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        return results