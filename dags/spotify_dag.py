from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

#Definicion del DAG 

# Agrega el path del dag y va a encontrar el main en src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Definir la función ANTES del DAG, fuera de cualquier bloque
def etl_spotify():
    """
    Función que ejecuta el pipeline o codigo de main.py
   
    """
    from main import run_pipeline
    
    print("Ejecutando ETL desde Airflow...")
    resultado = run_pipeline()
    print(f"✅ Pipeline completado: {len(resultado)} registros")
    
    return True

# Configuración del DAG
default_args = {
    "owner": "JesikaB",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": "mailstureport@sample.com",
    "retries": 3,
    "retry_delay": timedelta(minutes=3)
}

# Definir el DAG
with DAG(
    dag_id='spotify_etl',
    description="Pipeline ETL de Spotify - Proyecto Final",
    schedule_interval='@daily',  # Ejecuta todos los días a medianoche
    default_args=default_args,
    start_date=datetime(2025, 10, 1),  # Fecha específica, no timedelta
    catchup=False,  # No ejecutar fechas pasadas
    tags=['spotify', 'etl', 'final']
) as dag:
    
    # Definir la tarea DENTRO del bloque with
    run_etl_spotify = PythonOperator(
        task_id="etl_spotify",
        python_callable=etl_spotify,  # Ahora puede encontrar la función
    )

 