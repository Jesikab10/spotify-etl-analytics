"""CSV loader - Sin base de datos"""
import pandas as pd
from pathlib import Path
from datetime import datetime

class CSVLoader:
    def __init__(self, output_dir='data/outputs'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ CSV configurado: {output_dir}")
    
    def load_data(self, df_final, table_name='spotify_data'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{table_name}_{timestamp}.csv"
        filepath = self.output_dir / filename
        
        df_final.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✅ Guardado: {filepath} ({len(df_final)} filas)")
        
        # También latest para fácil acceso
        df_final.to_csv(self.output_dir / f"{table_name}_latest.csv", index=False)