import json  
import sqlite3  
import os  
  
class KnowledgeBase:  
    def __init__(self, db_path='knowledge.db'):  
        self.db_path = db_path  
        self.conn = sqlite3.connect(db_path)  
        self._create_tables()  
  
    def _create_tables(self):  
        cursor = self.conn.cursor()  
        cursor.execute('''  
            CREATE TABLE IF NOT EXISTS facts (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                claim TEXT UNIQUE,  
                source TEXT,  
                verified INTEGER DEFAULT 0  
            )  
        ''')  
        self.conn.commit()  
  
    def add_fact(self, claim, source='manual'):  
        cursor = self.conn.cursor()  
        try:  
            cursor.execute('INSERT INTO facts (claim, source, verified) VALUES (?, ?, 1)', (claim, source))  
            self.conn.commit()  
            return True  
        except sqlite3.IntegrityError:  
            return False  
  
    def verify_claim(self, claim):  
        cursor = self.conn.cursor()  
        cursor.execute('SELECT verified FROM facts WHERE claim = ?', (claim,))  
        result = cursor.fetchone()  
        if result:  
            return bool(result[0])  
        return False  
  
    def load_from_json(self, json_path):  
        if os.path.exists(json_path):  
            with open(json_path, 'r', encoding='utf-8') as f:  
                data = json.load(f)  
            for item in data:  
                self.add_fact(item['claim'], item.get('source', 'json_import'))  
  
    def close(self):  
