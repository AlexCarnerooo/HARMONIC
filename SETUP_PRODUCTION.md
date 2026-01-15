# 🌐 Guía Rápida: Acceder a Harmonic desde un Dominio

## 📋 Pasos para Deployment

### 1. Desplegar en Railway (Recomendado - Gratis)

#### Paso 1: Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con tu cuenta de GitHub
3. Click en "New Project"

#### Paso 2: Desplegar el Backend (Flask)
1. Click en "Deploy from GitHub repo"
2. Selecciona tu repositorio: `AlexCarnerooo/HARMONIC`
3. Railway detectará automáticamente que es Python
4. En **Settings** → **Root Directory**: selecciona `backend`
5. En **Settings** → **Start Command**: pon `gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
6. Railway te dará una URL como: `https://harmonic-backend-production.up.railway.app`
   - **¡Guarda esta URL!** La necesitarás después

#### Paso 3: Desplegar el Frontend Chat (Next.js)
1. En el mismo proyecto de Railway, click en "New Service"
2. Selecciona "Deploy from GitHub repo"
3. Selecciona el mismo repositorio: `AlexCarnerooo/HARMONIC`
4. En **Settings** → **Root Directory**: selecciona `frontend_chat`
5. Railway detectará que es Node.js
6. En **Settings** → **Variables**, añade:
   ```
   OPENAI_API_KEY=tu_api_key_de_openai
   NEXT_PUBLIC_FLASK_URL=https://harmonic-backend-production.up.railway.app
   ```
   (Reemplaza con la URL real de tu backend)
7. Railway te dará otra URL como: `https://harmonic-chat-production.up.railway.app`
   - **¡Guarda esta URL también!**

#### Paso 4: Actualizar la URL del Chat en el Código
1. Abre `frontend/index.html` en tu editor
2. Busca la línea que dice: `<meta name="chat-url" content="CHAT_URL_PLACEHOLDER">`
3. Reemplaza `CHAT_URL_PLACEHOLDER` con la URL de tu chat (ej: `https://harmonic-chat-production.up.railway.app`)
4. Guarda el archivo
5. Haz commit y push:
   ```bash
   git add frontend/index.html
   git commit -m "Actualizar URL del chat para producción"
   git push
   ```
6. Railway hará auto-deploy automáticamente

### 2. Acceder a tu Aplicación

Una vez desplegado:
- **URL Principal**: `https://harmonic-backend-production.up.railway.app`
  - Esta es la URL donde puedes acceder a toda la aplicación
  - El chat se cargará automáticamente desde el servicio Next.js

### 3. Configurar Dominio Personalizado (Opcional)

Si quieres un dominio personalizado (ej: `harmonic.tudominio.com`):

1. En Railway, ve a tu servicio del backend
2. Click en **Settings** → **Domains**
3. Click en "Custom Domain"
4. Añade tu dominio
5. Sigue las instrucciones para configurar DNS

## 🔧 Alternativa: Render.com

Si prefieres Render:

### Backend (Flask)
1. Ve a [render.com](https://render.com)
2. Click en "New" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: `harmonic-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Environment**: Python 3

### Frontend Chat (Next.js)
1. Click en "New" → "Web Service"
2. Conecta el mismo repositorio
3. Configuración:
   - **Name**: `harmonic-chat`
   - **Root Directory**: `frontend_chat`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Environment**: Node
   - **Environment Variables**:
     - `OPENAI_API_KEY=tu_api_key`
     - `NEXT_PUBLIC_FLASK_URL=https://harmonic-backend.onrender.com`

## ✅ Checklist

- [ ] Backend Flask desplegado y funcionando
- [ ] Frontend Chat (Next.js) desplegado y funcionando
- [ ] URL del chat actualizada en `frontend/index.html`
- [ ] Variables de entorno configuradas
- [ ] API Key de OpenAI configurada
- [ ] Probado acceso desde el navegador

## 🐛 Troubleshooting

### El chat no carga
- Verifica que la URL del chat en `frontend/index.html` sea correcta
- Verifica que `NEXT_PUBLIC_FLASK_URL` esté configurada en el servicio del chat
- Revisa los logs en Railway/Render para ver errores

### El backend no responde
- Verifica que el archivo CSV esté en el repositorio (`data/datos_procesados.csv`)
- Revisa los logs para ver errores de Python
- Verifica que todas las dependencias estén en `requirements.txt`

### CORS errors
- El código ya tiene CORS habilitado en Flask
- Si persisten errores, verifica que las URLs sean correctas

## 📞 Soporte

Si tienes problemas, revisa:
- Los logs en Railway/Render
- La consola del navegador (F12)
- El archivo `DEPLOYMENT.md` para más detalles
