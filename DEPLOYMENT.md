# 🚀 Guía de Deployment - Harmonic

Esta guía te ayudará a desplegar Harmonic en diferentes plataformas de hosting.

## 📋 Requisitos Previos

- Cuenta en GitHub
- Cuenta en una plataforma de hosting (Railway, Render, Heroku, etc.)
- API Key de OpenAI (para el chat)

## 🌐 Opciones de Hosting Recomendadas

### 1. **Railway** (Recomendado - Más fácil)
- ✅ Gratis con límites generosos
- ✅ Soporte para Python y Node.js
- ✅ Auto-deploy desde GitHub
- ✅ Variables de entorno fáciles de configurar

### 2. **Render**
- ✅ Plan gratuito disponible
- ✅ Soporte para múltiples servicios
- ✅ Auto-deploy desde GitHub

### 3. **Heroku**
- ⚠️ Ya no tiene plan gratuito
- ✅ Muy establecido y confiable
- ✅ Fácil de usar

## 🔧 Configuración para Railway

### Paso 1: Preparar el repositorio

1. Sube tu código a GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### Paso 2: Desplegar en Railway

1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta o inicia sesión con GitHub
3. Click en "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es un proyecto Python

### Paso 3: Configurar Variables de Entorno

En Railway, ve a tu proyecto → Settings → Variables y añade:

```
FLASK_ENV=production
PORT=5000
PYTHON_VERSION=3.9.18
```

### Paso 4: Configurar el Frontend Chat (Next.js)

Necesitarás un segundo servicio en Railway para el chat:

1. En Railway, click en "New Service" → "GitHub Repo"
2. Selecciona el mismo repositorio
3. En "Root Directory", selecciona `frontend_chat`
4. Railway detectará que es un proyecto Next.js
5. Añade las variables de entorno:
   - `OPENAI_API_KEY=tu_api_key_aqui`
   - `NEXT_PUBLIC_FLASK_URL=https://tu-backend.railway.app`

### Paso 5: Actualizar URLs en el código

Después de obtener las URLs de Railway, actualiza:
- `frontend/index.html`: Cambia `localhost:3000` por la URL de tu servicio Next.js
- `frontend_chat/app/api/chat/route.ts`: Cambia `localhost:5000` por la URL de tu servicio Flask

## 🔧 Configuración para Render

### Backend (Flask)

1. Ve a [render.com](https://render.com)
2. Crea una cuenta
3. Click en "New" → "Web Service"
4. Conecta tu repositorio de GitHub
5. Configuración:
   - **Name**: harmonic-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app_flask:app --bind 0.0.0.0:$PORT`
   - **Root Directory**: `backend`

### Frontend Chat (Next.js)

1. En Render, click en "New" → "Web Service"
2. Conecta el mismo repositorio
3. Configuración:
   - **Name**: harmonic-chat
   - **Environment**: Node
   - **Build Command**: `cd frontend_chat && npm install && npm run build`
   - **Start Command**: `cd frontend_chat && npm start`
   - **Root Directory**: `frontend_chat`
   - **Environment Variables**:
     - `OPENAI_API_KEY=tu_api_key`
     - `NEXT_PUBLIC_FLASK_URL=https://harmonic-backend.onrender.com`

## 📝 Variables de Entorno Necesarias

### Backend (Flask)
```
FLASK_ENV=production
PORT=5000
```

### Frontend Chat (Next.js)
```
OPENAI_API_KEY=tu_api_key_de_openai
NEXT_PUBLIC_FLASK_URL=https://tu-backend-url.com
NODE_ENV=production
```

## 🔄 Actualizar URLs después del Deployment

Una vez que tengas las URLs de producción, actualiza estos archivos:

1. **frontend/index.html**: Busca `localhost:3000` y reemplázalo con la URL de tu servicio Next.js
2. **frontend_chat/app/api/chat/route.ts**: Busca `localhost:5000` y reemplázalo con la URL de tu servicio Flask

## 🐛 Troubleshooting

### Error: "Module not found"
- Asegúrate de que `requirements.txt` tenga todas las dependencias
- Verifica que el build command instale las dependencias correctamente

### Error: "Port already in use"
- Usa la variable de entorno `$PORT` que proporciona la plataforma
- No hardcodees el puerto 5000

### El chat no se conecta al backend
- Verifica que `NEXT_PUBLIC_FLASK_URL` esté configurada correctamente
- Asegúrate de que CORS esté habilitado en Flask (ya está configurado)

### El CSV no se encuentra
- Verifica que `data/datos_procesados.csv` esté en el repositorio
- Asegúrate de que las rutas relativas sean correctas

## 📦 Estructura del Proyecto

```
SongRecommender-main/
├── backend/          # Flask API
├── frontend/         # HTML estático
├── frontend_chat/    # Next.js Chat
├── data/             # Datos CSV
├── Procfile          # Para Heroku/Railway
├── runtime.txt       # Versión de Python
└── requirements.txt  # Dependencias Python
```

## ✅ Checklist Pre-Deployment

- [ ] Código subido a GitHub
- [ ] Variables de entorno configuradas
- [ ] URLs actualizadas en el código
- [ ] `requirements.txt` actualizado
- [ ] `package.json` con scripts de build
- [ ] CORS configurado en Flask
- [ ] API Key de OpenAI configurada
- [ ] Archivo CSV incluido en el repositorio

## 🎉 ¡Listo!

Una vez desplegado, tu aplicación estará disponible públicamente en las URLs que te proporcione la plataforma de hosting.
