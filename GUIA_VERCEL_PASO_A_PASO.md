# ⚡ Guía Paso a Paso: Deploy en Vercel (Frontend)

## 📋 PASO A PASO en Vercel

### 1. Crear Proyecto en Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión (puedes usar GitHub)
2. Click en **"Add New Project"** o **"New Project"**
3. Conecta tu repositorio de GitHub
4. Selecciona el repositorio de SongRecommender

### 2. Configurar Root Directory

1. En la configuración del proyecto, busca **"Root Directory"**
2. Click en **"Edit"** o **"Override"**
3. Selecciona: **`frontend_chat`**
4. Esto le dice a Vercel que el proyecto Next.js está en esa carpeta

### 3. Configurar Framework Preset

Vercel debería detectar automáticamente que es Next.js, pero verifica:
- **Framework Preset**: `Next.js`
- **Build Command**: `npm run build` (automático)
- **Output Directory**: `.next` (automático)
- **Install Command**: `npm install` (automático)

### 4. Configurar Variables de Entorno

**IMPORTANTE**: Necesitas la URL de Railway primero.

Ve a **Settings → Environment Variables** y agrega:

#### Para Production (y Preview):

```
OPENAI_API_KEY=tu_api_key_real_de_openai
NEXT_PUBLIC_FLASK_URL=https://tu-proyecto.up.railway.app
NODE_ENV=production
```

**Reemplaza**:
- `tu_api_key_real_de_openai` → Tu API key real de OpenAI
- `https://tu-proyecto.up.railway.app` → La URL real de tu backend en Railway

#### Cómo agregar variables:

1. Click en **"Add New"**
2. **Key**: `OPENAI_API_KEY`
3. **Value**: Tu API key (ej: `sk-proj-...`)
4. Selecciona **Production**, **Preview**, y **Development**
5. Click en **"Save"**
6. Repite para `NEXT_PUBLIC_FLASK_URL` y `NODE_ENV`

### 5. Deploy

1. Click en **"Deploy"**
2. Vercel construirá el proyecto automáticamente
3. Espera a que termine el build (puede tardar 2-5 minutos)
4. Una vez completado, verás: **"Ready"**

### 6. Obtener el Dominio

1. Una vez deployado, Vercel te dará una URL automáticamente:
   ```
   https://tu-proyecto.vercel.app
   ```
2. **Copia esta URL** - la necesitarás para actualizar CORS en Railway

### 7. Actualizar CORS en Railway

Ahora que tienes la URL de Vercel, vuelve a Railway:

1. Ve a tu proyecto en Railway
2. **Variables → Edit**
3. Actualiza `CORS_ORIGINS`:

```
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

O si quieres permitir múltiples dominios:

```
CORS_ORIGINS=https://tu-proyecto.vercel.app,https://www.tudominio.com
```

4. Guarda y Railway hará un redeploy automático

---

## 🔍 Verificar que Funciona

1. Abre la URL de Vercel en tu navegador
2. Deberías ver el chat de HARMONIC GPT
3. Prueba escribir algo en el chat
4. Verifica que no haya errores de CORS en la consola del navegador (F12)

---

## 🐛 Troubleshooting

### Error: "NEXT_PUBLIC_FLASK_URL is not defined"

**Solución**:
- Verifica que la variable esté en **Environment Variables** de Vercel
- Asegúrate de que el nombre sea exactamente `NEXT_PUBLIC_FLASK_URL` (con `NEXT_PUBLIC_` al inicio)
- Redeploy después de agregar la variable

### Error: "Failed to fetch" o CORS error

**Solución**:
1. Verifica que `NEXT_PUBLIC_FLASK_URL` apunte a la URL correcta de Railway
2. Verifica que `CORS_ORIGINS` en Railway incluya la URL de Vercel
3. Asegúrate de que ambas URLs usen `https://` (no `http://`)

### Error: "OPENAI_API_KEY is missing"

**Solución**:
- Verifica que la variable esté configurada en Vercel
- Si no tienes API key, puedes usar `DUMMY_MODE=true` (pero agrega esto como variable de entorno también)

### El build falla

**Solución**:
- Revisa los logs de build en Vercel
- Verifica que `frontend_chat/package.json` exista
- Verifica que todas las dependencias estén instaladas

---

## ✅ Checklist

- [ ] Proyecto creado en Vercel
- [ ] Repositorio conectado
- [ ] Root Directory = `frontend_chat`
- [ ] Variables de entorno configuradas:
  - [ ] `OPENAI_API_KEY`
  - [ ] `NEXT_PUBLIC_FLASK_URL` (con URL de Railway)
  - [ ] `NODE_ENV=production`
- [ ] Build exitoso
- [ ] Dominio obtenido
- [ ] URL funciona en el navegador
- [ ] CORS actualizado en Railway con URL de Vercel
- [ ] Chat funciona correctamente

---

## 🔗 Conectar Dominio Personalizado (Opcional)

### En Vercel:

1. Ve a **Settings → Domains**
2. Agrega tu dominio (ej: `www.tudominio.com`)
3. Sigue las instrucciones para configurar DNS
4. Vercel te dará los registros DNS a agregar

### En Railway:

1. Ve a **Settings → Domains**
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones

### Actualizar CORS:

Actualiza `CORS_ORIGINS` en Railway para incluir tu dominio:

```
CORS_ORIGINS=https://www.tudominio.com,https://tu-proyecto.vercel.app
```

---

## 📝 Notas Importantes

- **Variables con `NEXT_PUBLIC_`** son accesibles en el cliente (navegador)
- **Variables sin `NEXT_PUBLIC_`** solo están disponibles en el servidor
- Después de agregar variables, Vercel hace redeploy automático
- El dominio de Vercel es gratuito y siempre termina en `.vercel.app`
- Puedes tener múltiples deployments (production, preview, development)

---

## 🎉 ¡Listo!

Tu aplicación debería estar funcionando en:
- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.up.railway.app`

Si todo funciona, ya tienes tu aplicación en producción. 🚀
