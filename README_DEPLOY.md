# 🚀 Guía de Deploy - CV Analyzer

## Configuración de Variables de Entorno

### 🔧 Desarrollo Local

1. **Copia el archivo de ejemplo:**
   ```bash
   cp env.example .env
   ```

2. **Edita el archivo `.env`:**
   ```env
   GEMINI_API_KEY=tu_api_key_real_de_gemini
   ```

3. **Ejecuta la aplicación:**
   ```bash
   streamlit run main.py
   ```

### ☁️ Deploy en Streamlit Cloud

#### Opción A: Configuración en Dashboard

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio de GitHub
3. En la configuración de la app, ve a **Secrets**
4. Agrega tu variable:
   ```toml
   GEMINI_API_KEY = "tu_api_key_real_de_gemini"
   ```

#### Opción B: Archivo de Configuración

1. Edita el archivo `.streamlit/secrets.toml`
2. Reemplaza `tu_api_key_aqui` con tu API key real:
   ```toml
   GEMINI_API_KEY = "tu_api_key_real_de_gemini"
   ```

### 🔑 Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la key y úsala en tu configuración

### 📁 Estructura de Archivos

```
ai-cv-analyzer/
├── .env                    # Variables locales (NO subir a git)
├── .streamlit/
│   └── secrets.toml       # Variables para Streamlit Cloud
├── env.example            # Ejemplo de configuración
├── main.py
├── analyzer.py
└── requirements.txt
```

### ✅ Verificación

La aplicación mostrará automáticamente:
- ✅ **Configuración de producción detectada** (en Streamlit Cloud)
- 🔧 **Modo desarrollo local** (en tu máquina local)

### 🚨 Solución de Problemas

**Error: "GEMINI_API_KEY no encontrada"**

1. Verifica que el archivo `.env` existe y tiene el formato correcto
2. Asegúrate de que la API key es válida
3. Reinicia la aplicación después de cambiar la configuración

**Error en Streamlit Cloud:**

1. Verifica que las variables están en la sección "Secrets"
2. Asegúrate de que el formato es correcto (con comillas)
3. Espera unos minutos para que los cambios se propaguen

### 🔒 Seguridad

- **NUNCA** subas tu API key real a GitHub
- El archivo `.env` está en `.gitignore` para evitar commits accidentales
- Usa diferentes API keys para desarrollo y producción

### 📝 Comandos Útiles

```bash
# Desarrollo local
streamlit run main.py

# Verificar configuración
python -c "from analyzer import get_api_key; print('API Key configurada:', bool(get_api_key()))"

# Deploy (solo push a GitHub)
git add .
git commit -m "Configuración para deploy"
git push origin main
``` 