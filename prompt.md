# CONTEXTO DEL PROYECTO: Sistema de Automatización Web Inteligente

## RESUMEN EJECUTIVO
Este es un sistema modular de automatización web que combina Selenium WebDriver con modelos de lenguaje de OpenAI. El sistema permite crear "tasks" independientes que realizan automatizaciones web con capacidades de toma de decisiones inteligentes mediante LLM.

## ARQUITECTURA DEL SISTEMA

### Estructura de Archivos:
```
proyecto/
├── venv/                     # Entorno virtual Python
├── utils/                    # Utilidades y drivers
│   ├── chromedriver         # WebDriver de Chrome
│   └── browser_data/        # Datos persistentes del navegador
├── tasks/                   # Tasks de automatización (AQUÍ VAN LAS NUEVAS TASKS)
│   ├── ejemplo.py          # Task básica de demostración
│   └── busqueda_inteligente.py # Task avanzada con múltiples búsquedas
├── functions/               # Funciones extra
│   └── llm.py              # Módulo de integración con OpenAI
├── presets.json            # Configuración global del sistema
├── .env                    # API keys y variables sensibles
├── main.py                 # Motor principal del sistema
├── ws                      # Script ejecutable para lanzar tasks
└── setup.sh               # Script de inicialización
```

### Flujo de Ejecución:
1. Usuario ejecuta: `./ws nombre_de_task`
2. Script `ws` verifica que la task existe
3. `main.py` importa dinámicamente la función `task()` del archivo
4. Se configura/reutiliza navegador Chrome con debugging remoto
5. Se ejecuta la task con todos los objetos de Selenium disponibles
6. El navegador se mantiene abierto para inspección manual

## ANATOMÍA DE UNA TASK

### Estructura Obligatoria:
Cada task debe ser un archivo Python en `tasks/` con una función principal:

```python
def task(presets, selenium_objects):
    """
    Función principal de la task
    
    Args:
        presets (dict): Configuración desde presets.json
        selenium_objects (dict): Objetos de Selenium y utilidades
    
    Returns:
        dict: Resultado de la automatización
    """
    # Extraer objetos necesarios
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    By = selenium_objects['By']
    EC = selenium_objects['EC']
    chat = selenium_objects['chat']  # Función para LLM
    
    # Tu código de automatización aquí
    
    return {"success": True, "data": "resultado"}
```

### Objetos Disponibles en selenium_objects:
- **driver**: WebDriver de Selenium (Chrome configurado)
- **wait**: WebDriverWait con timeout por defecto
- **By**: Localizadores de elementos (By.ID, By.CLASS_NAME, etc.)
- **EC**: Expected Conditions para esperas explícitas
- **chat**: Función para interactuar con OpenAI LLM

### Configuración Disponible en presets:
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

## USO DE LA FUNCIÓN LLM

### Sintaxis Básica:
```python
response = chat(presets['openai_model'], "Tu prompt aquí")

if response['success']:
    data = response['data']  # Respuesta parseada como JSON
    print(f"LLM respondió: {data}")
else:
    print(f"Error en LLM: {response['error']}")
```

### Estructura de Respuesta de chat():
```python
{
    "success": True/False,
    "data": {},  # Respuesta parseada como JSON
    "raw_content": "contenido_crudo",
    "model_used": "gpt-4o-mini",
    "tokens_used": 150,
    "error": "mensaje_de_error"  # Solo si success=False
}
```

### Mejores Prácticas para Prompts:
- Siempre especifica que quieres respuesta en JSON
- Sé específico sobre la estructura esperada
- Incluye ejemplos en el prompt si es necesario
- El sistema automáticamente parsea JSON de la respuesta

## CAPACIDADES DEL NAVEGADOR

### Características Especiales:
- **Reutilización Inteligente**: Detecta navegadores existentes y los reutiliza
- **Persistencia**: Cookies y sesiones se mantienen entre ejecuciones
- **Puerto de Debug**: Chrome corre con `--remote-debugging-port=9222`
- **Datos Persistentes**: Se guardan en `utils/browser_data/`
- **Anti-detección**: Configurado para evitar detección de automatización

### Elementos Típicos de Selenium:
```python
# Esperas explícitas (RECOMENDADO)
element = wait.until(EC.presence_of_element_located((By.ID, "mi-id")))
clickable = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn")))

# Seleccionar elementos
elementos = driver.find_elements(By.CSS_SELECTOR, "h3")
input_field = driver.find_element(By.NAME, "search")

# Interacciones
input_field.send_keys("texto")
input_field.send_keys(Keys.RETURN)
button.click()

# Screenshots
driver.save_screenshot("utils/captura.png")
```

## PATRONES COMUNES EN TASKS

### 1. Task de Web Scraping:
```python
def task(presets, selenium_objects):
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    
    # Navegar
    driver.get("https://sitio.com")
    
    # Extraer datos
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item")))
    
    # Procesar con LLM
    data = [elem.text for elem in elements]
    analysis = chat(presets['openai_model'], f"Analiza estos datos: {data}")
    
    return {"success": True, "data": analysis['data']}
```

### 2. Task de Formularios:
```python
def task(presets, selenium_objects):
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    chat = selenium_objects['chat']
    
    # LLM genera datos para el formulario
    form_data = chat(presets['openai_model'], "Genera datos para un formulario de contacto")
    
    # Llenar formulario
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    name_field.send_keys(form_data['data']['name'])
    
    return {"success": True}
```

### 3. Task de Análisis:
```python
def task(presets, selenium_objects):
    driver = selenium_objects['driver']
    chat = selenium_objects['chat']
    
    # Navegar y capturar contenido
    driver.get("https://sitio.com")
    content = driver.find_element(By.TAG_NAME, "body").text
    
    # LLM analiza el contenido
    analysis = chat(presets['openai_model'], f"Analiza este contenido: {content[:1000]}")
    
    return {"success": True, "analysis": analysis['data']}
```

## CONVENCIONES Y BUENAS PRÁCTICAS

### Nomenclatura:
- Nombres de tasks: `snake_case.py` (ej: `extraer_precios.py`)
- Función principal: siempre `task(presets, selenium_objects)`
- Variables: descriptivas y en español/inglés consistente

### Estructura de Retorno Recomendada:
```python
return {
    "success": True/False,
    "data": {},  # Datos principales extraídos/procesados
    "errors": [],  # Lista de errores encontrados
    "screenshots": [],  # Rutas de capturas tomadas
    "execution_time": time.time(),  # Timestamp de ejecución
    "llm_responses": [],  # Respuestas del LLM para debugging
    "metadata": {}  # Información adicional
}
```

### Manejo de Errores:
```python
try:
    # Código de automatización
    result = {"success": True}
except TimeoutException:
    result = {"success": False, "error": "Timeout esperando elemento"}
except NoSuchElementException:
    result = {"success": False, "error": "Elemento no encontrado"}
except Exception as e:
    result = {"success": False, "error": str(e)}

return result
```

### Logging Recomendado:
```python
print("🚀 Iniciando task...")
print("🌐 Navegando a sitio...")
print("🔍 Buscando elementos...")
print("🤖 Consultando LLM...")
print("✅ Task completada")
print("❌ Error encontrado")
```

## EJEMPLOS DE TASKS COMPLEJAS

El proyecto incluye dos ejemplos funcionales:
- **`ejemplo.py`**: Task básica con búsqueda en Google y análisis LLM
- **`busqueda_inteligente.py`**: Task avanzada con múltiples búsquedas y análisis comprensivo

## COMANDOS ÚTILES

```bash
# Ejecutar una task
./ws nombre_task

# Ver tasks disponibles
./ws

# Activar entorno virtual manualmente
source venv/bin/activate

# Instalar dependencias adicionales
pip install nueva-libreria
```

## LIMITACIONES Y CONSIDERACIONES

- Chrome debe estar instalado en el sistema
- ChromeDriver debe ser compatible con la versión de Chrome
- API key de OpenAI requerida en archivo .env
- El navegador se mantiene abierto intencionalmente para debugging
- Puerto 9222 debe estar disponible para debugging remoto
- Algunas páginas pueden detectar automatización a pesar de las medidas anti-detección

---

## INSTRUCCIONES PARA EL LLM ASISTENTE

Cuando te pidan crear una nueva task:

1. **Pregunta por el objetivo específico** de la automatización
2. **Identifica qué sitio web** será el objetivo
3. **Determina si necesita LLM** para toma de decisiones
4. **Crea la función task()** siguiendo la estructura obligatoria
5. **Incluye manejo de errores** robusto
6. **Usa las convenciones** de logging con emojis
7. **Retorna un diccionario** con la estructura recomendada
8. **Comenta el código** para explicar la lógica

El código debe ser funcional, robusto y seguir las mejores prácticas establecidas en este proyecto.