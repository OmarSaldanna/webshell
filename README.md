# 🚀 Sistema de Automatización Web con Selenium + OpenAI

Un sistema modular y inteligente para automatización web que combina Selenium con la potencia de los modelos de lenguaje de OpenAI.

## 🌟 Características

- **🔄 Reutilización inteligente de navegador**: Detecta y reutiliza instancias existentes de Chrome
- **🤖 Integración con OpenAI**: Usa LLM para decisiones inteligentes durante la automatización
- **📦 Arquitectura modular**: Tasks independientes y reutilizables
- **⚡ Ejecución sencilla**: Un comando para ejecutar cualquier task
- **🛠 Configuración flexible**: JSON centralizado para toda la configuración

## 📁 Estructura del Proyecto

```
proyecto/
├── venv/                   # Entorno virtual
├── utils/                  # Utilidades y drivers
│   ├── chromedriver       # WebDriver de Chrome
│   └── browser_data/      # Datos del navegador
├── tasks/                  # Tasks de automatización
│   └── ejemplo.py         # Task de ejemplo
├── presets.json           # Configuración principal
├── .env                   # Variables de entorno (API keys)
├── llm.py                 # Módulo de integración con OpenAI
├── main.py                # Archivo principal
├── ws                     # Script ejecutable para tasks
└── setup.sh              # Script de inicialización
```

## 🚀 Instalación y Configuración

### 1. Configuración inicial

```bash
# Hacer ejecutable y correr el script de setup
chmod +x setup.sh
./setup.sh
```

### 2. Configurar API Key de OpenAI

Edita el archivo `.env` y agrega tu clave de API:

```env
OPENAI_API_KEY=tu_clave_de_api_aqui
```

### 3. Descargar ChromeDriver

1. Ve a [ChromeDriver Downloads](https://chromedriver.chromium.org/)
2. Descarga la versión compatible con tu Chrome
3. Coloca el ejecutable en `utils/chromedriver`
4. Dale permisos de ejecución: `chmod +x utils/chromedriver`

## 🎯 Uso del Sistema

### Ejecutar una task

```bash
# Ejecutar la task de ejemplo
./ws ejemplo

# Ejecutar cualquier otra task
./ws nombre_de_mi_task
```

### Ver tasks disponibles

```bash
# Si ejecutas ws sin argumentos, muestra las tasks disponibles
./ws
```

## 📝 Crear una Nueva Task

1. Crea un archivo Python en `tasks/mi_nueva_task.py`
2. Implementa la función `task(presets, selenium_objects)`
3. Ejecuta con `./ws mi_nueva_task`

### Estructura de una Task

```python
def task(presets, selenium_objects):
    """
    Args:
        presets (dict): Configuración desde presets.json
        selenium_objects (dict): Objetos de Selenium
            - driver: WebDriver de Selenium
            - wait: WebDriverWait configurado
            - By: Selector de elementos
            - EC: Expected Conditions
            - chat: Función para LLM
    
    Returns:
        dict: Resultado de la automatización
    """
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    By = selenium_objects['By']
    EC = selenium_objects['EC']
    chat = selenium_objects['chat']
    
    # Tu código de automatización aquí
    driver.get("https://ejemplo.com")
    
    # Usar LLM para decisiones inteligentes
    response = chat(presets['openai_model'], "Tu prompt aquí")
    
    return {"success": True, "data": "resultado"}
```

## ⚙️ Configuración (presets.json)

```json
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
```

### Parámetros disponibles:

- **webdriver_path**: Ruta al ejecutable de ChromeDriver
- **openai_model**: Modelo de OpenAI a usar (gpt-4o-mini recomendado)
- **base_directory**: Directorio base del proyecto (vacío = directorio actual)
- **browser_port**: Puerto para debugging remoto de Chrome
- **browser_user_data**: Directorio para datos persistentes del navegador
- **default_timeout**: Timeout por defecto para esperas en Selenium
- **headless**: Ejecutar Chrome en modo headless (true/false)
- **window_size**: Tamaño de ventana [ancho, alto]

## 🤖 Uso de la Función LLM

```python
# Ejemplo de uso del chat con LLM
response = chat(
    presets['openai_model'], 
    "Analiza esta página web y dime qué elementos son más importantes"
)

if response['success']:
    data = response['data']  # Respuesta parseada como JSON
    print(f"Análisis: {data}")
else:
    print(f"Error: {response['error']}")
```

## 🔄 Reutilización de Navegador

El sistema detecta automáticamente si ya hay una instancia de Chrome abierta y la reutiliza:

- ✅ **Primera ejecución**: Abre nueva ventana de Chrome
- ✅ **Ejecuciones siguientes**: Reutiliza la ventana existente
- ✅ **Misma pestaña**: Ejecuta en la pestaña actual
- ✅ **Persistencia**: Los datos de sesión se mantienen

## 🛠 Troubleshooting

### Error: ChromeDriver no encontrado
```bash
# Verificar que ChromeDriver esté en la ruta correcta
ls -la utils/chromedriver
chmod +x utils/chromedriver
```

### Error: OpenAI API Key
```bash
# Verificar que la API key esté configurada
cat .env
```

### Error: Task no encontrada
```bash
# Verificar que el archivo existe
ls tasks/
```

### Error: Puerto ocupado
```bash
# Cambiar puerto en presets.json
# O cerrar instancias existentes de Chrome
pkill -f "chrome.*remote-debugging-port"
```

## 📊 Ejemplo de Task Completa

La task de ejemplo (`tasks/ejemplo.py`) demuestra:

- ✅ Navegación web básica
- ✅ Uso de LLM para decisiones inteligentes
- ✅ Búsqueda y análisis de contenido
- ✅ Captura de screenshots
- ✅ Manejo de errores
- ✅ Retorno de resultados estructurados

## 🚀 Ideas para Tasks

- **🔍 Web Scraping**: Extracción inteligente de datos
- **🤖 Chatbots**: Automatización de conversaciones
- **📊 Análisis**: Análisis automático de contenido web
- **📋 Formularios**: Llenado inteligente de formularios
- **🧪 Testing**: Pruebas automatizadas con validación por LLM
- **📈 Monitoreo**: Vigilancia de cambios en sitios web

## 📞 Soporte

Si encuentras algún problema:

1. Revisa los logs en la terminal
2. Verifica la configuración en `presets.json`
3. Asegúrate de que ChromeDriver sea compatible con tu versión de Chrome
4. Verifica que la API key de OpenAI esté configurada correctamente

## 💡 Tips y Mejores Prácticas

### Para Tasks eficientes:
- **🎯 Específicas**: Mantén cada task enfocada en una sola funcionalidad
- **🔄 Reutilizables**: Diseña tasks que puedan usarse con diferentes parámetros
- **🛡 Robustas**: Incluye manejo de errores y timeouts apropiados
- **📊 Informativas**: Retorna información útil sobre el resultado

### Para uso de LLM:
- **📝 Prompts claros**: Sé específico sobre el formato de respuesta esperado
- **🎛 Temperatura baja**: Para respuestas más consistentes y estructuradas  
- **⚡ Eficiencia**: Usa el modelo más simple que resuelva tu problema
- **🔄 Fallbacks**: Siempre ten un plan B si el LLM falla

### Para debugging:
- **📸 Screenshots**: Toma capturas en puntos clave para debugging
- **📋 Logs**: Usa prints informativos para seguir el flujo
- **⏱ Timeouts**: Ajusta timeouts según la velocidad del sitio web
- **🔍 Selectores**: Usa selectores CSS robustos que no cambien frecuentemente

## 🔧 Personalización Avanzada

### Modificar configuración de Chrome:
```python
# En main.py, función setup_browser()
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--start-maximized')
```

### Agregar nuevas utilidades:
```python
# En presets.json
"custom_wait_time": 5,
"screenshot_quality": 90,
"max_retries": 3
```

### Extender selenium_objects:
```python
# En main.py, antes de ejecutar la task
selenium_objects.update({
    'ActionChains': ActionChains,
    'Select': Select,
    'Keys': Keys
})
```

## 🌟 Funcionalidades Avanzadas

### Persistencia de datos entre ejecuciones:
- El navegador mantiene cookies y sesiones
- Los datos se guardan en `utils/browser_data/`
- Perfecto para tasks que requieren login

### Manejo inteligente de errores:
- Reconexión automática si se pierde la conexión
- Reintentos automáticos en fallos de red
- Fallbacks cuando el LLM no responde

### Escalabilidad:
- Fácil agregar nuevos modelos de LLM
- Soporte para múltiples navegadores
- Configuración por task individual

## 📚 Recursos Adicionales

- [Documentación de Selenium](https://selenium-python.readthedocs.io/)
- [API de OpenAI](https://platform.openai.com/docs)
- [ChromeDriver](https://chromedriver.chromium.org/)
- [Selectores CSS](https://www.w3schools.com/cssref/css_selectors.asp)

---

🎉 **¡Ya tienes todo listo para crear automatizaciones web inteligentes!**

Ejecuta `./ws ejemplo` para ver el sistema en acción.