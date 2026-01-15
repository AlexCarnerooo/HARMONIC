# 🚂 Guía Paso a Paso: Deploy en Railway (Backend)

## ✅ Cambios Realizados en el Código

1. ✅ **`backend/runtime.txt`** creado con `python-3.11.8`
2. ✅ **`backend/requirements.txt`** actualizado con versiones fijas (wheels)
3. ✅ **`railway.json`** actualizado con comando correcto

---

## 📋 PASO A PASO en Railway

### 1. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Conecta tu repositorio de GitHub
5. Selecciona la rama `main` (o `master`)

### 2. Configurar Root Directory

1. En tu servicio web, ve a **Settings**
2. Busca **"Root Directory"**
3. Configúralo como: **`backend`**
4. Guarda los cambios

### 3. Configurar Variables de Entorno

Ve a **Variables** y agrega:

```
CORS_ORIGINS=*
FLASK_ENV=production
```

**Nota**: `PORT` se asigna automáticamente, no lo configures.

### 4. Configurar Start Command (si Railway no lo detecta)

1. Ve a **Settings → Start Command**
2. Pega este comando exacto:

```
gunicorn app_flask:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Explicación**:
- `app_flask:app` = archivo `app_flask.py` con variable `app`
- `--bind 0.0.0.0:$PORT` = escucha en todas las interfaces, puerto dinámico
- `--workers 2` = 2 procesos worker
- `--timeout 120` = timeout de 120 segundos

### 5. Limpiar Cache y Redeploy

1. Ve a **Deployments**
2. Si hay opción **"Clear build cache"** o **"Clear cache"**, úsala
3. Click en **"Redeploy"** en el último deployment

### 6. Obtener el Dominio

1. Ve a **Settings → Networking** o **Settings → Domains**
2. Click en **"Generate Domain"** o **"Add Domain"**
3. Railway te dará una URL como:
   ```
   https://tu-proyecto.up.railway.app
   ```
4. **Copia esta URL** - la necesitarás para Vercel

---

## 🔍 Verificar que Funciona

1. Ve a **Deployments** y espera a que el build termine
2. Si hay errores, revisa los **Logs**
3. Una vez que diga **"Deployed"**, abre la URL en tu navegador
4. Deberías ver la página principal de Harmonic

---

## 🐛 Troubleshooting

### Error: "Failed building wheel for pandas"

**Solución**: 
- Verifica que `backend/runtime.txt` tenga `python-3.11.8`
- Verifica que `backend/requirements.txt` tenga las versiones actualizadas
- Limpia el cache y redeploy

### Error: "Module not found"

**Solución**:
- Verifica que Root Directory esté configurado como `backend`
- Verifica que `requirements.txt` esté en `backend/requirements.txt`

### Error: "Port already in use"

**Solución**:
- Railway asigna el puerto automáticamente, no lo configures manualmente
- Usa `$PORT` en el comando de inicio

### El servicio no inicia

**Solución**:
- Verifica el Start Command: debe ser `gunicorn app_flask:app --bind 0.0.0.0:$PORT`
- Revisa los logs en Railway para ver el error exacto

---

## ✅ Checklist

- [ ] Proyecto creado en Railway
- [ ] Repositorio conectado
- [ ] Root Directory = `backend`
- [ ] Variables de entorno configuradas (`CORS_ORIGINS`, `FLASK_ENV`)
- [ ] Start Command configurado
- [ ] Build exitoso
- [ ] Dominio obtenido
- [ ] URL funciona en el navegador

---

## 📝 Notas Importantes

- **No uses** `cd backend` en el Start Command si Root Directory ya está en `backend`
- **Python 3.11.8** es la versión recomendada para evitar compilaciones
- Las versiones en `requirements.txt` están optimizadas para wheels (instalación rápida)
- El dominio de Railway cambiará si eliminas y recreas el servicio

---

## 🎯 Siguiente Paso

Una vez que tengas la URL de Railway (ej: `https://tu-proyecto.up.railway.app`), 
sigue con la guía de Vercel para configurar el frontend.
