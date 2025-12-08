

import sqlite3
import os
from typing import List, Tuple, Optional


class Database:
    
    
    def __init__(self, db_path: str):

        self.db_path = db_path
        self._ensure_db_exists()
        self._create_tables()
    
    def _ensure_db_exists(self):
        
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def _create_tables(self):
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de jugadores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de puntuaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')
        
        # Índice para mejorar consultas de ranking
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_scores_score 
            ON scores(score DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_player(self, name: str) -> int:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO players (name) VALUES (?)', (name,))
            player_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # El jugador ya existe, obtener su ID
            cursor.execute('SELECT id FROM players WHERE name = ?', (name,))
            player_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return player_id
    
    def add_score(self, player_id: int, score: int, level: int) -> int:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scores (player_id, score, level)
            VALUES (?, ?, ?)
        ''', (player_id, score, level))
        
        score_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return score_id
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, int]]:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, s.score, s.level
            FROM scores s
            JOIN players p ON s.player_id = p.id
            ORDER BY s.score DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_player_scores(self, player_id: int, limit: int = 10) -> List[Tuple[int, int]]:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT score, level
            FROM scores
            WHERE player_id = ?
            ORDER BY score DESC
            LIMIT ?
        ''', (player_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_player_by_name(self, name: str) -> Optional[int]:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM players WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_total_players(self) -> int:

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM players')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_total_scores(self) -> int:
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM scores')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def clear_all_data(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM scores')
        cursor.execute('DELETE FROM players')
        
        conn.commit()
        conn.close()
