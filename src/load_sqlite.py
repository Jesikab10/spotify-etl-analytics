"""SQLite loader - Para desarrollo local"""
import sqlite3
import pandas as pd
from pathlib import Path

class SQLiteLoader:
    def __init__(self, db_path='data/spotify.db'):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        print(f"✅ SQLite conectado: {db_path}")
    
    def load_data(self, df_final, table_name='spotify_data'):
        df_final.to_sql(table_name, self.connection, if_exists='replace', index=False)
        print(f"✅ Cargados {len(df_final)} registros en {table_name}")
    
    def close(self):
        self.connection.close()