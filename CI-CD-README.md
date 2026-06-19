# 🚀 CI/CD y Despliegue en Vercel para J.A.R.V.I.S. HUD

Este directorio contiene la configuración para separar el frontend (React/Vite) y alojarlo en **Vercel**, manteniendo nuestro backend (FastAPI) en **Railway**.

## Beneficios de esta arquitectura:
1. **Caché CDN global automático:** Vercel optimiza los assets estáticos a nivel mundial.
2. **Build automático:** Ya no hace falta compilar manualmente en local ni usar `deploy-jarvis-hud.ps1` obligatoriamente. Todo `git push` a `main` disparará un build en la nube.
3. **Escalado independiente:** Si el tráfico de la interfaz sube, Vercel lo maneja gratis sin saturar el procesador de nuestro backend Python en Railway.

---

## 🛠️ PASO 1: Configurar Vercel

1. Ingrese a [Vercel](https://vercel.com/) e inicie sesión con GitHub.
2. Haga clic en **"Add New Project"**.
3. Importe su repositorio `axyntrax`.
4. En **Framework Preset**, Vercel detectará automáticamente Vite.
5. En **Root Directory**, haga clic en "Edit" y seleccione `jarvis_hud`.
6. En **Environment Variables**, añada:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://jarvis-ax-cloud-production.up.railway.app`
7. Haga clic en **Deploy**.

---

## 🛠️ PASO 2: Automatización con GitHub Actions (Opcional)

Si desea que **GitHub Actions** maneje el despliegue en Vercel por usted (usando el archivo `.github/workflows/deploy-jarvis-hud.yml`), necesita configurar los siguientes Secrets en su repositorio de GitHub:

Vaya a: **Settings** > **Secrets and variables** > **Actions** > **New repository secret**

| Nombre | Descripción |
|--------|-------------|
| `VERCEL_TOKEN` | Se genera en Vercel (Account Settings > Tokens) |
| `VERCEL_ORG_ID` | El ID de su organización en Vercel (Scope) |
| `VERCEL_PROJECT_ID` | El ID de su proyecto en Vercel (Settings > General) |
| `VITE_API_URL` | `https://jarvis-ax-cloud-production.up.railway.app` |

*(Nota: Si conectó Vercel directamente en el Paso 1, el Paso 2 no es estrictamente necesario, Vercel escuchará los commits automáticamente).*

---

## ✅ Soporte de CORS
El backend en `main.py` ya ha sido actualizado con `CORSMiddleware` para aceptar conexiones entrantes desde Vercel.
