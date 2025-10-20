"""Pipeline ETL Spotify"""
from extract import SpotifyExtractor
from transform import SpotifyTransformer

# ============ CONFIGURACIÓN - CAMBIA AQUÍ ===================================
LOADER_TYPE = 'sqlite'  # Opciones: 'sqlite', 'postgresql', 'csv', 'redshift'
# ============================================================================

def run_pipeline():
    print("Spotify ETL Pipeline -Running")
    
    # EXTRACT
    print("\n Consultando Artistas en Spotify...")
    extractor = SpotifyExtractor()
    artist_ids = ["790FomKkXshlbRYZFtlgla", "3qsKSpcV3ncke3hw52JSMB"]
    
    df_artists = extractor.get_artists(artist_ids)
    df_albums = extractor.get_albums(artist_ids)
    df_tracks = extractor.get_top_tracks(artist_ids)
    print(f"✅ {len(df_artists)} artistas, {len(df_albums)} álbumes, {len(df_tracks)} tracks")
    
    # TRANSFORM
    print("\n Obteniendo data requerida...")
    transformer = SpotifyTransformer()
    df_final = transformer.transform_all(df_artists, df_albums, df_tracks)
    print(f"✅ {len(df_final)} registros")
    
    # 1️⃣ SIEMPRE generar CSV
    print("\n💾 Guardando CSV para análisis...")
    from load_csv import CSVLoader
    csv_saver = CSVLoader() 
    csv_saver.load_data(df_final, table_name='spotify_data')

    # 2️⃣ LOAD adicional según selección (solo si no es CSV)
    if LOADER_TYPE != 'csv':
        print(f"\n🚀 Cargando datos en destino {LOADER_TYPE.upper()}...")
        if LOADER_TYPE == 'sqlite':
            from load_sqlite import SQLiteLoader
            loader = SQLiteLoader()
        elif LOADER_TYPE == 'postgresql':
            from load_postgresql import PostgreSQLLoader
            loader = PostgreSQLLoader()
        elif LOADER_TYPE == 'redshift':
            from load_redshift import RedshiftLoader
            loader = RedshiftLoader()
        else:
            raise ValueError(f"Loader desconocido: {LOADER_TYPE}")

        loader.load_data(df_final, table_name='spotify_data')
        if hasattr(loader, 'close'):
            loader.close()

    # 3️⃣ Siempre ejecutar análisis usando el CSV generado
    print("\n📈 Generando análisis a partir del CSV más reciente...")
    try:
        from analysis import run_analysis
        run_analysis(csv_path='data/outputs/spotify_data_latest.csv')
    except ImportError:
        print("\n⚠️  Módulo de análisis no disponible.")
    except Exception as e:
        print(f"\n⚠️  Error durante el análisis: {e}")

    print("\n✅ Pipeline completado.")
    return df_final

if __name__ == "__main__":
    run_pipeline()