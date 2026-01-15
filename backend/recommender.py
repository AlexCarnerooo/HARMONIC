import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import os

class SongRecommender:
    def __init__(self):
        # Obtener la ruta absoluta al directorio del proyecto
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(current_dir, 'data', 'datos_procesados.csv')
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encontró el archivo de datos en: {data_path}")
            
        self.df = pd.read_csv(data_path)
        
        # Verificar que tenemos todas las columnas originales necesarias
        required_original_columns = ['year_original', 'popularity_original', 
                                   'duration_ms_original', 'loudness_original', 
                                   'tempo_original']
        missing_columns = [col for col in required_original_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Faltan columnas originales en el CSV: {missing_columns}")
            
        self.numeric_features = ['acousticness', 'danceability', 'duration_ms', 
                               'instrumentalness', 'liveness', 'loudness', 
                               'popularity', 'speechiness', 'tempo']
        
        # Inicializar diccionario de modelos KNN por cluster
        self.knn_models = {}
        
    def _get_cluster_knn(self, cluster_id):
        """Obtener o crear el modelo KNN para un cluster específico."""
        if cluster_id not in self.knn_models:
            # Filtrar canciones del cluster
            cluster_songs = self.df[self.df['cluster'] == cluster_id]
            
            if len(cluster_songs) < 6:
                # Si el cluster es muy pequeño, usar todas las canciones
                cluster_songs = self.df
            
            # Crear y entrenar modelo KNN para este cluster
            knn = NearestNeighbors(n_neighbors=min(6, len(cluster_songs)), metric='euclidean')
            knn.fit(cluster_songs[self.numeric_features])
            
            self.knn_models[cluster_id] = {
                'model': knn,
                'indices': cluster_songs.index
            }
            
        return self.knn_models[cluster_id]
        
    def _convert_to_json_serializable(self, song_dict):
        """Convertir valores numpy a tipos Python nativos."""
        return {k: float(v) if isinstance(v, np.number) else v for k, v in song_dict.items()}
        
    def find_songs(self, name):
        """
        Buscar todas las canciones que coincidan con el nombre o artista.
        
        Args:
            name (str): Nombre de la canción o artista
            
        Returns:
            list: Lista de diccionarios con información de las canciones encontradas
        """
        # Buscar por nombre de canción (ignorando mayúsculas/minúsculas)
        name_matches = self.df[self.df['name'].str.lower() == name.lower()].copy()
        
        # Buscar por artista (ignorando mayúsculas/minúsculas)
        artist_matches = self.df[self.df['artists'].str.lower().str.contains(name.lower(), na=False)].copy()
        
        # Combinar ambos resultados y eliminar duplicados
        matches = pd.concat([name_matches, artist_matches]).drop_duplicates()
        
        if matches.empty:
            return []
            
        # Convertir todas las coincidencias a formato serializable
        results = []
        for _, song in matches.iterrows():
            result = self._convert_to_json_serializable(song.to_dict())
            result['index'] = int(song.name)  # song.name es el índice
            
            # Usar valores originales
            result['year'] = int(song['year_original'])
            result['popularity'] = float(song['popularity_original'])
            result['duration_ms'] = int(song['duration_ms_original'])
            result['loudness'] = float(song['loudness_original'])
            result['tempo'] = float(song['tempo_original'])
            
            results.append(result)
            
        # Ordenar por año de más reciente a más antiguo
        results.sort(key=lambda x: x['year'], reverse=True)
        return results
    
    def get_popular_songs(self, limit=20):
        """
        Obtener las canciones más populares.
        
        Args:
            limit (int): Número de canciones a retornar
            
        Returns:
            list: Lista de diccionarios con información de las canciones populares
        """
        # Ordenar por popularidad descendente
        popular_songs = self.df.nlargest(limit, 'popularity_original')
        
        results = []
        for _, song in popular_songs.iterrows():
            result = self._convert_to_json_serializable(song.to_dict())
            result['index'] = int(song.name)
            
            # Usar valores originales
            result['year'] = int(song['year_original'])
            result['popularity'] = float(song['popularity_original'])
            result['duration_ms'] = int(song['duration_ms_original'])
            result['loudness'] = float(song['loudness_original'])
            result['tempo'] = float(song['tempo_original'])
            
            results.append(result)
            
        return results
    
    def get_songs_by_mood(self, mood, limit=10):
        """
        Obtener canciones filtradas por estado de ánimo basado en atributos musicales.
        
        Args:
            mood (str): Estado de ánimo ('ansiedad', 'nervios', 'triste', 'feliz', 'energético', 'relajado')
            limit (int): Número de canciones a retornar
            
        Returns:
            list: Lista de diccionarios con información de las canciones filtradas
        """
        mood = mood.lower()
        filtered_df = self.df.copy()
        
        # Definir filtros por estado de ánimo basados en atributos musicales
        # Nota: El CSV no tiene columna 'energy', usamos 'danceability' y 'liveness' como proxies
        if mood in ['ansiedad', 'nervios', 'estrés', 'estres', 'tranquilidad', 'tranquilo', 'calma', 'relajante', 'relajado']:
            # Para ansiedad/nervios: bajo tempo, alta acousticness, baja danceability, bajo loudness
            filtered_df = filtered_df[
                (filtered_df['tempo_original'] < 90) &  # Tempo lento
                (filtered_df['acousticness'] > 0.5) &    # Alta acousticness
                (filtered_df['danceability'] < 0.5) &     # Baja danceability (más calmada)
                (filtered_df['loudness_original'] > -15)  # No muy fuerte
            ]
            # Ordenar por acousticness descendente y tempo ascendente
            filtered_df = filtered_df.sort_values(['acousticness', 'tempo_original'], ascending=[False, True])
            
        elif mood in ['triste', 'tristeza', 'depresión', 'depresion']:
            # Para tristeza: tempo medio-bajo, baja danceability, alta acousticness
            filtered_df = filtered_df[
                (filtered_df['tempo_original'] < 100) &
                (filtered_df['danceability'] < 0.6) &
                (filtered_df['acousticness'] > 0.4)
            ]
            filtered_df = filtered_df.sort_values(['acousticness', 'tempo_original'], ascending=[False, True])
            
        elif mood in ['feliz', 'alegría', 'alegria']:
            # Para felicidad: tempo medio-alto, alta danceability, bajo acousticness (más electrónica)
            filtered_df = filtered_df[
                (filtered_df['tempo_original'] > 100) &
                (filtered_df['danceability'] > 0.6) &
                (filtered_df['acousticness'] < 0.5)  # Menos acústica = más electrónica/energética
            ]
            filtered_df = filtered_df.sort_values(['danceability', 'tempo_original'], ascending=[False, False])
            
        elif mood in ['energético', 'energia', 'energía', 'focus', 'concentración', 'concentracion']:
            # Para energía: tempo alto, alta danceability, bajo acousticness
            filtered_df = filtered_df[
                (filtered_df['tempo_original'] > 120) &
                (filtered_df['danceability'] > 0.7) &
                (filtered_df['acousticness'] < 0.4)  # Menos acústica = más electrónica
            ]
            filtered_df = filtered_df.sort_values(['danceability', 'tempo_original'], ascending=[False, False])
            
        else:
            # Si no se reconoce el estado de ánimo, devolver canciones populares
            return self.get_popular_songs(limit)
        
        # Limitar resultados
        filtered_df = filtered_df.head(limit)
        
        # Convertir a formato JSON
        results = []
        for _, song in filtered_df.iterrows():
            result = self._convert_to_json_serializable(song.to_dict())
            result['index'] = int(song.name)
            
            # Usar valores originales
            result['year'] = int(song['year_original'])
            result['popularity'] = float(song['popularity_original'])
            result['duration_ms'] = int(song['duration_ms_original'])
            result['loudness'] = float(song['loudness_original'])
            result['tempo'] = float(song['tempo_original'])
            
            results.append(result)
        
        return results
    
    def search_suggestions(self, query, limit=10):
        """
        Buscar sugerencias de canciones y artistas para autocompletado.
        
        Args:
            query (str): Texto de búsqueda
            limit (int): Número máximo de sugerencias
            
        Returns:
            list: Lista de sugerencias con nombre y artista
        """
        if not query or len(query) < 2:
            return []
        
        query_lower = query.lower()
        
        # Buscar en nombres de canciones
        name_matches = self.df[
            self.df['name'].str.lower().str.contains(query_lower, na=False)
        ].head(limit)
        
        # Buscar en artistas
        artist_matches = self.df[
            self.df['artists'].str.lower().str.contains(query_lower, na=False)
        ].head(limit)
        
        # Combinar y eliminar duplicados
        matches = pd.concat([name_matches, artist_matches]).drop_duplicates(subset=['name', 'artists']).head(limit)
        
        suggestions = []
        for _, song in matches.iterrows():
            suggestions.append({
                'name': song['name'],
                'artists': song['artists'],
                'index': int(song.name)
            })
        
        return suggestions
    
    def get_songs_by_feature(self, feature, limit=20):
        """
        Obtener canciones filtradas por características musicales específicas.
        
        Args:
            feature (str): Característica ('recent', 'danceable', 'acoustic', 'high-energy', 'instrumental', 'live', 'speech')
            limit (int): Número de canciones a retornar
            
        Returns:
            list: Lista de diccionarios con información de las canciones filtradas
        """
        filtered_df = self.df.copy()
        
        if feature == 'recent':
            # Canciones recientes (últimos 10 años)
            current_year = 2024  # Ajustar según sea necesario
            min_year = current_year - 10
            filtered_df = filtered_df[filtered_df['year_original'] >= min_year]
            filtered_df = filtered_df.sort_values(['year_original', 'popularity_original'], ascending=[False, False])
            
        elif feature == 'danceable':
            # Alta danceability (música para bailar)
            filtered_df = filtered_df[filtered_df['danceability'] > 0.7]
            filtered_df = filtered_df.sort_values(['danceability', 'popularity_original'], ascending=[False, False])
            
        elif feature == 'acoustic':
            # Alta acousticness (música acústica)
            filtered_df = filtered_df[filtered_df['acousticness'] > 0.5]
            filtered_df = filtered_df.sort_values(['acousticness', 'popularity_original'], ascending=[False, False])
            
        elif feature == 'high-energy':
            # Alta energía (alta danceability y tempo)
            filtered_df = filtered_df[
                (filtered_df['danceability'] > 0.7) &
                (filtered_df['tempo_original'] > 120)
            ]
            filtered_df = filtered_df.sort_values(['danceability', 'tempo_original'], ascending=[False, False])
            
        elif feature == 'instrumental':
            # Alta instrumentalness (música instrumental)
            filtered_df = filtered_df[filtered_df['instrumentalness'] > 0.5]
            filtered_df = filtered_df.sort_values(['instrumentalness', 'popularity_original'], ascending=[False, False])
            
        elif feature == 'live':
            # Alta liveness (grabaciones en vivo)
            filtered_df = filtered_df[filtered_df['liveness'] > 0.3]
            filtered_df = filtered_df.sort_values(['liveness', 'popularity_original'], ascending=[False, False])
            
        elif feature == 'speech':
            # Alta speechiness (música con habla)
            filtered_df = filtered_df[filtered_df['speechiness'] > 0.3]
            filtered_df = filtered_df.sort_values(['speechiness', 'popularity_original'], ascending=[False, False])
            
        else:
            # Si no se reconoce la característica, devolver canciones populares
            return self.get_popular_songs(limit)
        
        # Limitar resultados
        filtered_df = filtered_df.head(limit)
        
        # Convertir a formato JSON
        results = []
        for _, song in filtered_df.iterrows():
            result = self._convert_to_json_serializable(song.to_dict())
            result['index'] = int(song.name)
            
            # Usar valores originales
            result['year'] = int(song['year_original'])
            result['popularity'] = float(song['popularity_original'])
            result['duration_ms'] = int(song['duration_ms_original'])
            result['loudness'] = float(song['loudness_original'])
            result['tempo'] = float(song['tempo_original'])
            result['danceability'] = float(song['danceability'])
            result['acousticness'] = float(song['acousticness'])
            
            results.append(result)
        
        return results
    
    def get_recommendations(self, song_idx):
        """
        Obtener 5 canciones similares dada una canción.
        
        Args:
            song_idx (int): Índice de la canción en el DataFrame
            
        Returns:
            list: Lista de diccionarios con información de las canciones recomendadas
        """
        try:
            # Obtener el cluster de la canción
            song_cluster = self.df.loc[song_idx, 'cluster']
            
            # Obtener el modelo KNN para este cluster
            cluster_knn = self._get_cluster_knn(song_cluster)
            
            # Obtener las características de la canción
            song_features = self.df.iloc[song_idx][self.numeric_features].values.reshape(1, -1)
            
            # Encontrar los vecinos más cercanos
            distances, indices = cluster_knn['model'].kneighbors(song_features)
            
            # Convertir índices locales del cluster a índices globales
            global_indices = cluster_knn['indices'][indices[0]]
            
            # Excluir la primera canción (que es la misma) y tomar las siguientes 5
            recommendations = []
            for idx, distance in zip(global_indices[1:], distances[0][1:]):
                song_info = self._convert_to_json_serializable(self.df.iloc[idx].to_dict())
                song_info['index'] = int(idx)
                song_info['distance'] = float(distance)
                
                # Usar valores originales
                song_info['year'] = int(song_info['year_original'])
                song_info['popularity'] = float(song_info['popularity_original'])
                song_info['duration_ms'] = int(song_info['duration_ms_original'])
                song_info['loudness'] = float(song_info['loudness_original'])
                song_info['tempo'] = float(song_info['tempo_original'])
                
                recommendations.append(song_info)
                
            return recommendations
        except IndexError:
            raise ValueError(f"No se encuentra la canción con índice {song_idx}")

# Ejemplo de uso:
if __name__ == "__main__":
    # Inicializar el recomendador
    recommender = SongRecommender()
    
    # Buscar todas las versiones de una canción
    song_name = "Yesterday"
    songs = recommender.find_songs(song_name)
    
    if songs:
        print(f"Versiones encontradas de '{song_name}':")
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['name']} ({song['year']}) por {song['artists']}")
            print(f"   Popularidad: {song['popularity']:.1f}%")
            print(f"   Duración: {song['duration_ms']/1000:.1f}s")
            print(f"   Volumen: {song['loudness']:.1f}dB")
            print(f"   Tempo: {song['tempo']:.1f}BPM")
        
        # Elegir una versión (por ejemplo, la primera)
        selected_song = songs[0]
        print(f"\nSeleccionada: {selected_song['name']} ({selected_song['year']}) por {selected_song['artists']}")
        
        # Obtener recomendaciones
        recommendations = recommender.get_recommendations(selected_song['index'])
        
        print("\nCanciones recomendadas:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['name']} ({rec['year']}) por {rec['artists']}")
            print(f"   Popularidad: {rec['popularity']:.1f}%")
            print(f"   Duración: {rec['duration_ms']/1000:.1f}s")
            print(f"   Volumen: {rec['loudness']:.1f}dB")
            print(f"   Tempo: {rec['tempo']:.1f}BPM")
            print(f"   Similitud: {(1 - rec['distance']) * 100:.1f}%") 