#!/bin/bash

# 🚀 Script de inicialización del proyecto de automatización web
echo "🚀 Iniciando configuración del proyecto de automatización web..."

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# Instalar librerías necesarias
echo "📚 Instalando librerías necesarias..."
pip install -r requirements.txt

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p utils
mkdir -p tasks

# Crear archivos principales
echo "📄 Creando archivos de configuración..."

# Crear presets.json
cat > presets.json << 'EOF'
{
    "webdriver_path": "./utils/chromedriver",
    "openai_model": "gpt-4o-mini",
    "base_directory": "",
    "browser_port": 9222,
    "browser_user_data": "./utils/browser_data",
    "default_timeout": 10,
    "headless": false,
    "window_size": [1920, 1080]
}
EOF

# Crear archivo .env para la API key de OpenAI
cat > .env << 'EOF'
OPENAI_API_KEY=tu_api_key_aqui
EOF

# Crear archivo ws ejecutable
cat > ws << 'EOF'
#!/bin/bash

# 🎯 Web Scraping Task Runner
if [ $# -eq 0 ]; then
    echo "❌ Error: Debes proporcionar el nombre de una task"
    echo "💡 Uso: ./ws <nombre_de_task>"
    echo "📋 Tasks disponibles:"
    ls tasks/*.py 2>/dev/null | sed 's/tasks\///g' | sed 's/\.py//g' | sed 's/^/   - /'
    exit 1
fi

TASK_NAME=$1
SCRIPT_DIR=" ***** here where the project is located ***** "
TASK_FILE="$SCRIPT_DIR/tasks/$TASK_NAME.py"

# Verificar que la task existe
if [ ! -f "$TASK_FILE" ]; then
    echo "❌ Error: La task '$TASK_NAME' no existe"
    echo "📁 Archivo esperado: $TASK_FILE"
    echo "📋 Tasks disponibles:"
    ls tasks/*.py 2>/dev/null | sed 's/tasks\///g' | sed 's/\.py//g' | sed 's/^/   - /'
    exit 1
fi

echo "🚀 Ejecutando task: $TASK_NAME"
cd "$SCRIPT_DIR"
source venv/bin/activate
python main.py "$TASK_NAME"
EOF

# Dar permisos de ejecución al script ws
chmod +x ws

echo ""
echo "✅ ¡Proyecto configurado exitosamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. 🔑 Edita el archivo .env y agrega tu OPENAI_API_KEY"
echo "2. 🌐 Descarga ChromeDriver y colócalo en utils/chromedriver"
echo "3. 🚀 Ejecuta una task con: ./ws ejemplo"
echo ""
echo "📁 Estructura creada:"
echo "   ├── venv/"
echo "   ├── utils/"
echo "   ├── tasks/"
echo "   ├── presets.json"
echo "   ├── .env"
echo "   └── ws (ejecutable)"
echo ""