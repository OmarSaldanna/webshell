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
SCRIPT_DIR="/Users/omarsaldanna/webshell"
TASK_FILE="$SCRIPT_DIR/tasks/$TASK_NAME.py"

echo ">>>> $TASK_FILE"

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
