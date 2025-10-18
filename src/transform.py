"""
Transformación de datos de Spotify
Responsabilidad: SOLO limpiar y preparar datos para análisis
"""

import pandas as pd

class SpotifyTransformer:
    """Transforma datos de Spotify en formato analítico"""
    
    def transform_all(self, df_artists, df_albums, df_tracks):
        """
        Aplica todas las transformaciones necesarias.
        
        Args:
            df_artists: DataFrame con datos de artistas
            df_albums: DataFrame con datos de álbumes
            df_tracks: DataFrame con datos de tracks
            
        Returns:
            DataFrame único con todos los datos limpios y etiquetados
        """
        # 1. Agregar columna de tipo para identificar cada sección
        df_artists = df_artists.copy()
        df_albums = df_albums.copy()
        df_tracks = df_tracks.copy()
        
        df_artists["Tipo"] = "Artista"
        df_albums["Tipo"] = "Álbum"
        df_tracks["Tipo"] = "Top Track"
        
        print(f"   Etiquetados: {len(df_artists)} artistas, {len(df_albums)} álbumes, {len(df_tracks)} tracks")
        
        # 2. Concatenar todos los DataFrames en uno solo
        df_final = pd.concat([df_artists, df_albums, df_tracks], ignore_index=True)
        
        # 3. Extraer primer género de la lista (si existe)
        if 'genres' in df_final.columns:
            df_final['genres'] = df_final['genres'].apply(
                lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x
            )
        
        # 4. Rellenar valores nulos con "no data"
        df_final = df_final.fillna("no data")
        
        print(f"   Transformaciones aplicadas: {len(df_final)} registros totales")
        
        return df_final
    
