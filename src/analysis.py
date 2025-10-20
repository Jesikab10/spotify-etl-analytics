"""
Analisis de datos de Spotify
Genera visualizaciones y metricas de engagement
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuracion visual
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def calcular_engagement_rate(df):
    """
    Calcula engagement rate: popularidad / seguidores
    Mayor engagement = conexion mas fuerte con audiencia
    """
    df_artists = df[df['Tipo'] == 'Artista'].copy()
    
    # Extraer numero de followers
    df_artists['followers_count'] = df_artists['followers'].apply(
        lambda x: eval(x)['total'] if isinstance(x, str) else 0
    )
    
    # Engagement rate normalizado
    df_artists['engagement_rate'] = (
        df_artists['popularity'] / df_artists['followers_count'] * 1000000
    )
    
    return df_artists[['name', 'popularity', 'followers_count', 'engagement_rate']]

def visualizar_comparativa(df_artists, output_dir='images'):
    """Dashboard comparativo de artistas"""
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Spotify Analytics Dashboard', fontsize=16, fontweight='bold')
    
    # Followers
    axes[0, 0].bar(df_artists['name'], df_artists['followers_count'], color=['#1DB954', '#FF6B6B'])
    axes[0, 0].set_title('Total Followers')
    axes[0, 0].set_ylabel('Seguidores')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Popularity
    axes[0, 1].bar(df_artists['name'], df_artists['popularity'], color=['#1DB954', '#FF6B6B'])
    axes[0, 1].set_title('Popularity Score')
    axes[0, 1].set_ylabel('Popularidad (0-100)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Engagement Rate
    axes[1, 0].bar(df_artists['name'], df_artists['engagement_rate'], color=['#1DB954', '#FF6B6B'])
    axes[1, 0].set_title('Engagement Rate (Insight Clave)')
    axes[1, 0].set_ylabel('Engagement')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Comparacion proporcional
    metrics = ['Followers', 'Popularity', 'Engagement']
    values_karol = [
        df_artists[df_artists['name'] == 'KAROL G']['followers_count'].values[0] / 1000000,
        df_artists[df_artists['name'] == 'KAROL G']['popularity'].values[0],
        df_artists[df_artists['name'] == 'KAROL G']['engagement_rate'].values[0]
    ]
    values_miko = [
        df_artists[df_artists['name'] == 'Young Miko']['followers_count'].values[0] / 1000000,
        df_artists[df_artists['name'] == 'Young Miko']['popularity'].values[0],
        df_artists[df_artists['name'] == 'Young Miko']['engagement_rate'].values[0]
    ]
    
    x = range(len(metrics))
    axes[1, 1].plot(x, values_karol, marker='o', label='KAROL G', linewidth=2)
    axes[1, 1].plot(x, values_miko, marker='s', label='Young Miko', linewidth=2)
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(metrics)
    axes[1, 1].set_title('Perfil Comparativo')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/dashboard_completo.png', dpi=300, bbox_inches='tight')
    print(f"   Dashboard: {output_dir}/dashboard_completo.png")
    plt.close()

def analizar_generos(df, output_dir='images'):
    """Analisis de distribucion de generos"""
    Path(output_dir).mkdir(exist_ok=True)
    
    df_artists = df[df['Tipo'] == 'Artista'].copy()
    
    # Extraer generos
    all_genres = []
    for genres in df_artists['genres']:
        if isinstance(genres, str):
            genre_list = eval(genres)
            all_genres.extend(genre_list)
    
    genre_counts = pd.Series(all_genres).value_counts()
    
    plt.figure(figsize=(10, 6))
    genre_counts.head(8).plot(kind='barh', color='#1DB954')
    plt.title('Distribución de Géneros Musicales', fontsize=14, fontweight='bold')
    plt.xlabel('Frecuencia')
    plt.ylabel('Género')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/analisis_generos.png', dpi=300, bbox_inches='tight')
    print(f"   Géneros: {output_dir}/analisis_generos.png")
    plt.close()
    
    return genre_counts

def generar_reporte(df_artists, genre_counts):
    """Genera insights clave"""
    karol = df_artists[df_artists['name'] == 'KAROL G'].iloc[0]
    miko = df_artists[df_artists['name'] == 'Young Miko'].iloc[0]
    
    print("\n📊 INSIGHTS PRINCIPALES:")
    print(f"   • Young Miko: {miko['engagement_rate']/karol['engagement_rate']:.1f}x mas engagement que KAROL G")
    print(f"   • KAROL G: {karol['followers_count']/miko['followers_count']:.1f}x mas audiencia absoluta")
    print(f"   • Géneros dominantes: {', '.join(genre_counts.head(3).index.tolist())}")

def run_analysis(csv_path='data/outputs/spotify_data_test.csv'):
    """
    Ejecuta analisis completo y genera visualizaciones
    
    Args:
        csv_path: Ruta al CSV con datos procesados
    """
    print("\n📈 Generando análisis y visualizaciones...")
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    
    # Calcular metricas
    df_artists = calcular_engagement_rate(df)
    
    # Generar visualizaciones
    visualizar_comparativa(df_artists)
    genre_counts = analizar_generos(df)
    
    # Mostrar insights
    generar_reporte(df_artists, genre_counts)
    
    print("✅ Análisis completado\n")

if __name__ == "__main__":
    run_analysis()
