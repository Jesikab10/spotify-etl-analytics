"""Pipeline ETL Spotify"""
from extract import SpotifyExtractor
from transform import SpotifyTransformer

# ============ CONFIGURACIÓN - CAMBIA AQUÍ ============
LOADER_TYPE = 'sqlite'  # Opciones: 'sqlite', 'postgresql', 'csv'
# =====================================================

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
    
    # LOAD - Selector automático
    print(f"\n Cargando en su seleccion: {LOADER_TYPE.upper()}...")
    
    if LOADER_TYPE == 'sqlite':
        from load_sqlite import SQLiteLoader
        loader = SQLiteLoader()
    elif LOADER_TYPE == 'postgresql':
        from load_postgresql import PostgreSQLLoader
        loader = PostgreSQLLoader()  
    elif LOADER_TYPE == 'csv':
        from load_csv import CSVLoader
        loader = CSVLoader()
    else:
        raise ValueError(f"Loader desconocido # Opciones: 'sqlite', 'postgresql', 'csv': {LOADER_TYPE}")
    
    loader.load_data(df_final)
    
    if hasattr(loader, 'close'):
        loader.close()
    
    print("\n✅ Pipeline completado")
    return df_final

if __name__ == "__main__":
    run_pipeline()