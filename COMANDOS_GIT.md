# 📝 Comandos Git para Deployment

## ✅ Pasos para subir cambios a GitHub

### 1. Ver qué archivos cambiaron
```bash
git status
```

### 2. Agregar todos los cambios
```bash
git add .
```

### 3. Hacer commit
```bash
git commit -m "Arreglar inicialización lazy y rutas del frontend para Railway"
```

### 4. Subir a GitHub
```bash
git push origin main
```

**Nota**: Si tu rama se llama `master` en lugar de `main`, usa:
```bash
git push origin master
```

---

## 🔍 Verificar qué rama estás usando

```bash
git branch
```

La rama actual tendrá un asterisco (*) al lado.

---

## ⚠️ Si hay errores

### Error: "nothing to commit"
Significa que no hay cambios nuevos. Verifica con:
```bash
git status
```

### Error: "branch is ahead"
Significa que tienes commits locales que no se han subido. Haz:
```bash
git push origin main
```

### Error: "authentication failed"
Necesitas autenticarte con GitHub. Usa:
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```
