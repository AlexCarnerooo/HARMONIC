# 🚂 Guía Paso a Paso: Desplegar Harmonic en Railway (GRATIS)

## 📋 Requisitos Previos

- ✅ Cuenta de GitHub (ya la tienes)
- ✅ Repositorio en GitHub: `AlexCarnerooo/HARMONIC` (ya está subido)
- ✅ API Key de OpenAI (para el chat)

---

## 🎯 PASO 1: Crear Cuenta en Railway

1. Ve a **[railway.app](https://railway.app)**
2. Click en **"Start a New Project"** o **"Login"**
3. Selecciona **"Login with GitHub"**
4. Autoriza Railway para acceder a tus repositorios
5. ¡Listo! Ya estás en Railway

---

## 🎯 PASO 2: Desplegar el Backend (Flask)

### 2.1 Crear el Servicio del Backend

1. En Railway, click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona tu repositorio: **`HARMONIC`**
4. Railway empezará a desplegar automáticamente

### 2.2 Configurar el Backend Correctamente

1. Click en el servicio que acabas de crear
2. Ve a la pestaña **"Settings"** (Configuración)
3. Busca **"Root Directory"** y escribe: `backend`
4. Busca **"Start Command"** y escribe:
   ```
   gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```
5. Click en **"Save"** o **"Deploy"**

### 2.3 Obtener la URL del Backend

1. Ve a la pestaña **"Settings"**
2. Busca **"Domains"** o **"Generate Domain"**
3. Click en **"Generate Domain"** (si no aparece automáticamente)
4. Railway te dará una URL como: `https://harmonic-production-xxxx.up.railway.app`
5. **¡COPIA ESTA URL!** La necesitarás después
   - Ejemplo: `https://harmonic-backend-production.up.railway.app`

### 2.4 Verificar que el Backend Funciona

1. Abre la URL que te dio Railway en tu navegador
2. Deberías ver la página principal de Harmonic
3. Si ves errores, revisa la pestaña **"Deployments"** para ver los logs

---

## 🎯 PASO 3: Desplegar el Frontend Chat (Next.js)

### 3.1 Crear el Servicio del Chat

1. En el **mismo proyecto** de Railway, click en **"New"** → **"Service"**
2. Selecciona **"GitHub Repo"**
3. Selecciona el mismo repositorio: **`HARMONIC`**
4. Railway empezará a desplegar

### 3.2 Configurar el Chat Correctamente

1. Click en el nuevo servicio del chat
2. Ve a **"Settings"**
3. En **"Root Directory"**, escribe: `frontend_chat`
4. Railway detectará automáticamente que es Node.js

### 3.3 Configurar Variables de Entorno del Chat

1. En la pestaña **"Variables"** del servicio del chat
2. Click en **"New Variable"** y añade estas dos:

   **Variable 1:**
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `tu_api_key_de_openai_aqui`
   - (Reemplaza con tu API key real de OpenAI)

   **Variable 2:**
   - **Name**: `NEXT_PUBLIC_FLASK_URL`
   - **Value**: `https://harmonic-backend-production.up.railway.app`
   - (Reemplaza con la URL REAL que obtuviste en el Paso 2.3)

3. Click en **"Add"** para cada variable
4. Railway reiniciará automáticamente el servicio

### 3.4 Obtener la URL del Chat

1. Ve a **"Settings"** del servicio del chat
2. Busca **"Domains"** o **"Generate Domain"**
3. Click en **"Generate Domain"**
4. Railway te dará otra URL como: `https://harmonic-chat-production.up.railway.app`
5. **¡COPIA ESTA URL TAMBIÉN!**

---

## 🎯 PASO 4: Actualizar la URL del Chat en el Código

### 4.1 Editar el Archivo HTML

1. En tu computadora, abre el archivo: `frontend/index.html`
2. Busca esta línea (alrededor de la línea 6):
   ```html
   <meta name="chat-url" content="CHAT_URL_PLACEHOLDER">
   ```
3. Reemplaza `CHAT_URL_PLACEHOLDER` con la URL del chat que obtuviste en el Paso 3.4
   - Ejemplo: `<meta name="chat-url" content="https://harmonic-chat-production.up.railway.app">`

### 4.2 Subir los Cambios a GitHub

1. Abre tu terminal en la carpeta del proyecto
2. Ejecuta estos comandos:
   ```bash
   git add frontend/index.html
   git commit -m "Actualizar URL del chat para Railway"
   git push
   ```

### 4.3 Railway Hace Auto-Deploy

- Railway detectará automáticamente el cambio en GitHub
- Espera 1-2 minutos mientras se despliega
- Verás el progreso en la pestaña **"Deployments"**

---

## 🎯 PASO 5: ¡Probar tu Aplicación!

1. Abre la URL del **backend** en tu navegador
   - Ejemplo: `https://harmonic-backend-production.up.railway.app`
2. Deberías ver:
   - ✅ La página principal de Harmonic
   - ✅ El menú de navegación funcionando
   - ✅ El chat cargando correctamente
   - ✅ Todas las funciones funcionando

---

## 🐛 Solución de Problemas

### El backend no carga
- ✅ Verifica que el **Root Directory** sea `backend`
- ✅ Verifica que el **Start Command** sea correcto
- ✅ Revisa los **logs** en la pestaña "Deployments"

### El chat no carga
- ✅ Verifica que `NEXT_PUBLIC_FLASK_URL` tenga la URL correcta del backend
- ✅ Verifica que `OPENAI_API_KEY` esté configurada
- ✅ Espera 2-3 minutos después de configurar las variables (Railway necesita reiniciar)

### Error "Module not found"
- ✅ Verifica que el archivo `data/datos_procesados.csv` esté en el repositorio
- ✅ Verifica que `requirements.txt` tenga todas las dependencias

### El chat muestra error de conexión
- ✅ Verifica que la URL del backend en `NEXT_PUBLIC_FLASK_URL` sea correcta
- ✅ Verifica que el backend esté funcionando (abre su URL directamente)

---

## 💰 ¿Es Realmente Gratis?

**Sí, Railway tiene un plan gratuito que incluye:**
- ✅ $5 de crédito gratis cada mes
- ✅ Suficiente para proyectos pequeños/medianos
- ✅ Si te quedas sin crédito, puedes añadir una tarjeta (pero no se cobra automáticamente)

**Para este proyecto:**
- El backend Flask consume muy poco
- El chat Next.js consume un poco más
- Con $5 deberías tener suficiente para varias semanas/meses

---

## 📝 Resumen de URLs que Necesitas

Después de completar todos los pasos, tendrás:

1. **URL del Backend**: `https://harmonic-backend-production.up.railway.app`
   - Esta es la URL principal donde accedes a tu app

2. **URL del Chat**: `https://harmonic-chat-production.up.railway.app`
   - Esta URL está configurada en el código HTML

---

## ✅ Checklist Final

- [ ] Backend Flask desplegado en Railway
- [ ] URL del backend guardada
- [ ] Frontend Chat desplegado en Railway
- [ ] Variables de entorno configuradas (OPENAI_API_KEY y NEXT_PUBLIC_FLASK_URL)
- [ ] URL del chat guardada
- [ ] `frontend/index.html` actualizado con la URL del chat
- [ ] Cambios subidos a GitHub
- [ ] Aplicación funcionando correctamente

---

## 🎉 ¡Listo!

Tu aplicación Harmonic ya está disponible públicamente en Railway. Cualquiera puede acceder usando la URL del backend.

¿Necesitas ayuda con algún paso específico? ¡Dime en qué paso estás y te ayudo!
