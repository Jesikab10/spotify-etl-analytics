"""
Carga de datos a Redshift
Responsabilidad: SOLO conectarse a DB y subir datos
"""

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

class RedshiftLoader:
    """Carga datos a AWS Redshift"""
    
    def __init__(self):
        """Configura conexión a Redshift desde .env"""
        load_dotenv()
        self.host = os.getenv("HOST_REDSHIFT")
        self.port = int(os.getenv("PORT_REDSHIFT"))
        self.database = "data-engineer-database"
        self.user = os.getenv("USER_REDSHIFT")
        self.password = os.getenv("PASS_REDSHIFT")
        self.schema = "jesika_berroteran_coderhouse"
        
        # Crear engine SQLAlchemy
        self.engine = create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        )
        print(f"✅ Redshift conectado: {self.host}/{self.database}")
    
    def load_data(self, df_final, table_name, if_exists='replace'):
        """
        Carga DataFrame a Redshift
        
        Args:
            df_final: DataFrame a cargar
            table_name: Nombre de la tabla
            if_exists: 'replace', 'append', o 'fail'
        """
        
        df_final.to_sql(table_name, self.engine, if_exists=if_exists,schema=self.schema, index=False)
        print(f"Redshift: Cargados {len(df_final)} registros en {self.schema}.{table_name}")