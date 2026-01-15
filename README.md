# 🎵 Harmonic - Music Therapy Platform

Plataforma de recomendación musical basada en atributos musicales reales de Spotify, con integración de chat GPT para recomendaciones personalizadas.

## ✨ Características

- 🎼 **Recomendaciones Musicales**: Basadas en atributos reales de canciones (tempo, danceability, acousticness, etc.)
- 💬 **Chat GPT Integrado**: Asistente inteligente para recomendaciones musicales personalizadas
- 🎯 **Búsqueda Avanzada**: Filtra por artista, década, tempo, popularidad
- 📰 **Noticias y Artículos**: Sección de noticias sobre música y salud mental
- ❤️ **Favoritos**: Guarda tus canciones favoritas
- 🎨 **Exploración por Características**: Descubre música por popularidad, recientes, para bailar, acústicas, etc.

## 🚀 Inicio Rápido

### Requisitos

- Python 3.9+
- Node.js 18+
- API Key de OpenAI (para el chat)

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/harmonic.git
cd harmonic
```

2. **Configurar Backend (Flask)**
```bash
cd backend
pip install -r requirements.txt
python app_flask.py
```

El servidor Flask estará disponible en `http://localhost:5000`

3. **Configurar Frontend Chat (Next.js)**
```bash
cd frontend_chat
npm install
# Crear archivo .env.local con tu API key de OpenAI
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env.local
npm run dev
```

El servidor Next.js estará disponible en `http://localhost:3000`

4. **Abrir la aplicación**
Abre `frontend/index.html` en tu navegador o accede a través del servidor Flask en `http://localhost:5000`

## 📦 Estructura del Proyecto

```
harmonic/
├── backend/              # API Flask con lógica de recomendación
│   ├── app_flask.py     # Servidor Flask principal
│   ├── recommender.py   # Clase SongRecommender con lógica ML
│   └── requirements.txt # Dependencias Python
├── frontend/            # Frontend HTML estático
│   ├── index.html       # Página principal
│   ├── newspaper-2035.html
│   └── article-detail-2035.html
├── frontend_chat/       # Aplicación Next.js para el chat
│   ├── app/            # Rutas y componentes Next.js
│   └── components/     # Componentes React
├── data/               # Datos CSV con información de canciones
│   └── datos_procesados.csv
└── DEPLOYMENT.md       # Guía detallada de deployment
```

## 🌐 Deployment

Para desplegar la aplicación en producción, consulta la [Guía de Deployment](DEPLOYMENT.md).

### Opciones de Hosting Recomendadas

- **Railway** (Recomendado): Fácil setup, auto-deploy desde GitHub
- **Render**: Plan gratuito disponible, soporte multi-servicio
- **Heroku**: Establecido y confiable (requiere plan de pago)

### Variables de Entorno Necesarias

**Backend:**
- `FLASK_ENV=production`
- `PORT=5000` (o el puerto que asigne la plataforma)

**Frontend Chat:**
- `OPENAI_API_KEY=tu_api_key_de_openai`
- `NEXT_PUBLIC_FLASK_URL=https://tu-backend-url.com`
- `NODE_ENV=production`

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask (Python), Pandas, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Chat**: Next.js 14, React, OpenAI API
- **ML**: K-Nearest Neighbors para recomendaciones

## 📊 Datos

El proyecto utiliza datos reales de Spotify procesados en `data/datos_procesados.csv`, incluyendo:
- Atributos musicales (tempo, danceability, acousticness, etc.)
- Metadatos (artista, año, popularidad)
- Clusters para recomendaciones basadas en similitud

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

Tu nombre - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- Spotify por los datos de atributos musicales
- OpenAI por la API de GPT
- La comunidad de código abierto
