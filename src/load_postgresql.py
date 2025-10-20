"""PostgreSQL loader - Para producción"""
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

class PostgreSQLLoader:
    def __init__(self):
        load_dotenv()
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "spotify")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        
        conn_str = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(conn_str)
        print(f"✅ PostgreSQL conectado: {host}:{port}/{db}")
    
    def load_data(self, df_final, table_name='spotify_data'):
        df_final.to_sql(table_name, self.engine, if_exists='replace', index=False)
        print(f"✅ Cargados {len(df_final)} registros en {table_name}")