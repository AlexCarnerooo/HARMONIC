# 🚀 Guía de Deployment: Vercel (Frontend) + Railway (Backend)

Esta guía te ayudará a desplegar tu aplicación en Vercel (frontend Next.js) y Railway (backend Flask).

## 📋 Cambios Realizados

### 1. Backend (Flask) - Preparado para Railway

✅ **CORS configurado**: Ahora acepta orígenes desde variables de entorno (`CORS_ORIGINS`)
✅ **Puerto dinámico**: Usa `0.0.0.0:$PORT` automáticamente desde Railway
✅ **Sin secretos hardcodeados**: Todas las configuraciones usan variables de entorno
✅ **Gunicorn configurado**: Listo para producción con `gunicorn_config.py`

### 2. Frontend (Next.js) - Preparado para Vercel

✅ **Variables de entorno**: Usa `NEXT_PUBLIC_FLASK_URL` para conectar con el backend
✅ **Vercel.json**: Configuración lista para Vercel
✅ **Sin URLs hardcodeadas**: Todas las URLs usan variables de entorno
✅ **Next.config.js**: Configurado para exponer variables públicas

### 3. Seguridad

✅ **.gitignore actualizado**: Asegura que no se suban archivos `.env` con secretos
✅ **Archivos .env.example**: Documentan todas las variables necesarias

---

## 🔧 Paso 1: Desplegar Backend en Railway

### 1.1 Crear cuenta y proyecto en Railway

1. Ve a [railway.app](https://railway.app) y crea una cuenta
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Conecta tu repositorio y selecciona la rama `main` (o `master`)

### 1.2 Configurar el servicio

Railway detectará automáticamente que es un proyecto Python. Configura:

**Settings → Root Directory**: `backend`

**Settings → Start Command**: 
```bash
gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

O usa el archivo `railway.json` que ya está configurado.

### 1.3 Configurar Variables de Entorno en Railway

Ve a **Variables** y agrega:

```
CORS_ORIGINS=https://tu-app.vercel.app,https://www.tudominio.com
FLASK_ENV=production
```

**Nota**: `PORT` se asigna automáticamente por Railway, no necesitas configurarlo.

### 1.4 Obtener la URL del Backend

1. Ve a **Settings → Domains**
2. Railway te dará una URL como: `https://tu-proyecto.railway.app`
3. **Copia esta URL**, la necesitarás para el frontend

---

## 🎨 Paso 2: Desplegar Frontend en Vercel

### 2.1 Crear cuenta y proyecto en Vercel

1. Ve a [vercel.com](https://vercel.com) y crea una cuenta
2. Click en "Add New Project"
3. Conecta tu repositorio de GitHub
4. Selecciona el directorio `frontend_chat` como **Root Directory**

### 2.2 Configurar Variables de Entorno en Vercel

Ve a **Settings → Environment Variables** y agrega:

```
OPENAI_API_KEY=tu_api_key_de_openai_aqui
NEXT_PUBLIC_FLASK_URL=https://tu-proyecto.railway.app
NODE_ENV=production
```

**Importante**: 
- Reemplaza `https://tu-proyecto.railway.app` con la URL real de tu backend en Railway
- `NEXT_PUBLIC_FLASK_URL` debe empezar con `https://` (no `http://`)

### 2.3 Desplegar

1. Click en "Deploy"
2. Vercel construirá y desplegará automáticamente
3. Obtendrás una URL como: `https://tu-proyecto.vercel.app`

### 2.4 Actualizar CORS en Railway

Una vez que tengas la URL de Vercel, vuelve a Railway y actualiza `CORS_ORIGINS`:

```
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

O si tienes múltiples dominios:

```
CORS_ORIGINS=https://tu-proyecto.vercel.app,https://www.tudominio.com
```

---

## 🔗 Paso 3: Conectar un Dominio Personalizado (Opcional)

### 3.1 En Vercel

1. Ve a tu proyecto en Vercel
2. **Settings → Domains**
3. Agrega tu dominio (ej: `www.tudominio.com`)
4. Sigue las instrucciones para configurar los DNS

### 3.2 En Railway

1. Ve a tu proyecto en Railway
2. **Settings → Domains**
3. Agrega tu dominio personalizado
4. Configura los DNS según las instrucciones

### 3.3 Actualizar CORS

Actualiza `CORS_ORIGINS` en Railway para incluir tu dominio:

```
CORS_ORIGINS=https://www.tudominio.com,https://tu-proyecto.vercel.app
```

---

## 📝 Comandos de Deployment

### Para Railway (Backend)

No necesitas comandos manuales. Railway hace el deploy automáticamente cuando haces push a GitHub.

**Para forzar un redeploy**:
1. Ve a tu proyecto en Railway
2. Click en "Deployments"
3. Click en "Redeploy" en el último deployment

### Para Vercel (Frontend)

**Deploy automático desde GitHub**:
```bash
# Simplemente haz push a tu repositorio
git add .
git commit -m "Preparar para deployment"
git push origin main
```

**Deploy manual con Vercel CLI** (opcional):
```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend_chat
vercel --prod
```

---

## ✅ Checklist de Verificación

### Backend (Railway)
- [ ] Proyecto creado en Railway
- [ ] Root Directory configurado como `backend`
- [ ] Variables de entorno configuradas (`CORS_ORIGINS`, `FLASK_ENV`)
- [ ] URL del backend obtenida y funcionando
- [ ] CORS configurado con la URL de Vercel

### Frontend (Vercel)
- [ ] Proyecto creado en Vercel
- [ ] Root Directory configurado como `frontend_chat`
- [ ] Variables de entorno configuradas:
  - [ ] `OPENAI_API_KEY`
  - [ ] `NEXT_PUBLIC_FLASK_URL` (con la URL de Railway)
  - [ ] `NODE_ENV=production`
- [ ] Deploy exitoso
- [ ] Frontend se conecta correctamente al backend

### Pruebas
- [ ] El frontend carga correctamente
- [ ] El chat funciona (prueba con una pregunta)
- [ ] Las recomendaciones musicales funcionan
- [ ] No hay errores de CORS en la consola del navegador

---

## 🐛 Troubleshooting

### Error: CORS bloqueado

**Solución**: Asegúrate de que `CORS_ORIGINS` en Railway incluya exactamente la URL de Vercel (con `https://` y sin barra final).

### Error: No se puede conectar al backend

**Solución**: 
1. Verifica que `NEXT_PUBLIC_FLASK_URL` en Vercel sea correcta
2. Asegúrate de que la URL empiece con `https://`
3. Verifica que el backend esté funcionando en Railway

### Error: OPENAI_API_KEY no encontrada

**Solución**: 
1. Verifica que la variable esté configurada en Vercel
2. Asegúrate de que el nombre sea exactamente `OPENAI_API_KEY` (sin espacios)

### El backend no inicia en Railway

**Solución**:
1. Verifica que el Root Directory esté configurado como `backend`
2. Verifica que `requirements.txt` esté en `backend/requirements.txt`
3. Revisa los logs en Railway para ver el error específico

---

## 📚 Archivos de Configuración Creados/Modificados

### Nuevos archivos:
- `frontend_chat/vercel.json` - Configuración de Vercel
- `DEPLOYMENT_VERCEL_RAILWAY.md` - Esta guía

### Archivos modificados:
- `backend/app_flask.py` - CORS configurable, puerto dinámico
- `frontend_chat/next.config.js` - Variables de entorno públicas
- `frontend_chat/env.example` - Documentación de variables
- `.gitignore` - Mejorado para excluir archivos .env
- `backend/nixpacks.toml` - Configuración para Railway

---

## 🎉 ¡Listo!

Tu aplicación debería estar funcionando en:
- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.railway.app`

Si tienes problemas, revisa los logs en Railway y Vercel para más detalles.
