from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from recommender import SongRecommender
import os

app = Flask(__name__)

# Configurar CORS para permitir Vercel y otros orígenes
allowed_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
CORS(app, origins=allowed_origins, supports_credentials=True)

# Inicializar el recomendador
recommender = SongRecommender()

@app.route('/')
def home():
    # Servir el frontend desde la carpeta padre
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/noticia-musica-salud')
def noticia_musica_salud():
    # Servir la página de noticias
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    return send_from_directory(frontend_path, 'noticia-musica-salud.html')

@app.route('/newspaper-2035')
def newspaper_2035():
    # Servir el periódico estilo NY Times de 2035
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    return send_from_directory(frontend_path, 'newspaper-2035.html')

@app.route('/article-detail-2035')
def article_detail_2035():
    # Servir el artículo detallado
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    return send_from_directory(frontend_path, 'article-detail-2035.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    # Servir imágenes estáticas
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'images')
    return send_from_directory(frontend_path, filename)

@app.route('/api/find-song', methods=['POST'])
def find_song():
    data = request.get_json()
    name = data.get('name', '')
    
    if not name:
        return jsonify({'error': 'Se requiere un nombre de canción'}), 400
        
    try:
        songs = recommender.find_songs(name)
        return jsonify(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    song_idx = data.get('song_idx')
    
    if song_idx is None:
        return jsonify({'error': 'Se requiere un índice de canción'}), 400
        
    try:
        recommendations = recommender.get_recommendations(song_idx)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/popular-songs', methods=['GET'])
def popular_songs():
    try:
        limit = request.args.get('limit', 20, type=int)
        songs = recommender.get_popular_songs(limit)
        return jsonify(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-suggestions', methods=['GET'])
def search_suggestions():
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        suggestions = recommender.search_suggestions(query, limit)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/songs-by-mood', methods=['GET'])
def songs_by_mood():
    try:
        mood = request.args.get('mood', '')
        limit = request.args.get('limit', 10, type=int)
        if not mood:
            return jsonify({'error': 'Se requiere un estado de ánimo'}), 400
        songs = recommender.get_songs_by_mood(mood, limit)
        return jsonify(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/songs-by-feature', methods=['GET'])
def songs_by_feature():
    try:
        feature = request.args.get('feature', '')
        limit = request.args.get('limit', 20, type=int)
        if not feature:
            return jsonify({'error': 'Se requiere una característica'}), 400
        songs = recommender.get_songs_by_feature(feature, limit)
        return jsonify(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 