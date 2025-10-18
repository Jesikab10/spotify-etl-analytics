"""
Extracción de datos desde Spotify API
Responsabilidad: SOLO comunicarse con la API de Spotify
"""

from dotenv import load_dotenv
import os
import base64
import requests
import pandas as pd

class SpotifyExtractor:
    """Extrae datos de Spotify API"""
    
    def __init__(self):
        """Inicializa credenciales desde .env"""
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None  # Nueva linea
    
    def get_token(self):
        """
        Obtiene access token de Spotify
        """
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

        token_headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        token_data = {
            "grant_type": "client_credentials",
            "redirect_uri": "https://localhost:8080/recal",
            "code": "code"
        }

        response = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")  # Nueva linea
            token_type = token_data.get("token_type")    # Nueva linea
        else:
            print("Error en la solicitud:")
            print("Código de estado:", response.status_code)

    def get_artists(self, artist_ids):
        """
        Extrae información de artistas
        """
        artist_ids_list = "%2C".join(artist_ids)
        country = "ES"
        auth_headers = {"Authorization": "Bearer " + self.token}  # Nueva linea
        url = f"https://api.spotify.com/v1/artists?ids={artist_ids_list}"

        response = requests.get(url, headers=auth_headers)  # Nueva linea

        if response.status_code == 200:
            data_artist = response.json()
            artists = data_artist.get("artists", [])
            
            if artists:
                lista_artistas = []
                for artist in artists:
                    lista_artistas.append(artist)
                return lista_artistas
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return []

    def get_albums(self, artist_ids):
        """Extrae álbumes de artistas"""
        artist_albums_url = "https://api.spotify.com/v1/artists/{}/albums"
        lista_albums = []
        auth_headers = {"Authorization": "Bearer " + self.token}  # Nueva linea

        for artist_id in artist_ids:  # Cambiado de artists_ids a artist_ids # Nueva linea
            response = requests.get(artist_albums_url.format(artist_id), headers=auth_headers)  # Nueva linea

            if response.status_code == 200:
                data_albums = response.json()
                albums = data_albums.get("items", [])   
                for album_info in albums:
                    album_info["artist_id"] = artist_id
                    search_terms = ["name", "id", "release_date", "total_tracks", "type", "artists","popularity"]
                    for term in search_terms:
                        if term == "artists":
                            artists_info = album_info.get("artists", [])
                            artist_list = []
                            for artist in artists_info:
                                artist_details = {
                                    "id": artist.get("id"),
                                    "name": artist.get("name"),
                                    "type": artist.get("type"),
                                    "release_date": artist.get("release_date"),
                                    "total_tracks": artist.get("total_tracks")
                                }
                                artist_list.append(artist_details)  # Nueva linea: mover append antes de asignar
                            album_info[term] = artist_list  # Nueva linea
                        else:
                            album_info[term] = album_info.get(term, None)
                    
                    lista_albums.append(album_info)
                
            else:
                print("Error en la solicitud:")
                print("Código de estado:", response.status_code)
                print("Contenido de la respuesta:", response.text)

        df_albums = pd.DataFrame(lista_albums)
        df_albums = df_albums[['name', 'release_date', 'total_tracks', 'popularity']]
        return df_albums  # Nueva linea

    def get_top_tracks(self, artist_ids):
        """Extrae top tracks de artistas"""
        artist_top_tracks_url = "https://api.spotify.com/v1/artists/{}/top-tracks"
        auth_headers = {"Authorization": "Bearer " + self.token}  # Nueva linea

        lista_top_tracks = []

        for artist_id in artist_ids:  # Cambiado de artists_ids a artist_ids # Nueva linea
            response = requests.get(
                artist_top_tracks_url.format(artist_id),
                headers=auth_headers,  # Nueva linea
                params={"country": "US"}
            )

            if response.status_code == 200:
                top_tracks_data = response.json()
                for track_info in top_tracks_data["tracks"]:
                    track_info["artist_id"] = artist_id
                    lista_top_tracks.append(track_info)
            else:
                print(f"Error en la solicitud para el artista {artist_id}:")
                print("Código de estado:", response.status_code)
                print("Contenido de la respuesta:", response.text)

        df_top_tracks = pd.DataFrame(lista_top_tracks)
        df_top_tracks = df_top_tracks[["id", "name", "popularity","artist_id"]]
        return df_top_tracks  # Nueva linea






    
