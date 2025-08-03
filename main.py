#!/usr/bin/env python3

import sys
import json
import os
import importlib.util
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Importar función de LLM
from functions.llm import chat

# Variables globales para mantener el navegador
driver = None
current_task = None

def load_presets():
    """Cargar configuración desde presets.json"""
    try:
        with open('presets.json', 'r', encoding='utf-8') as f:
            presets = json.load(f)
        
        # Si base_directory está vacío, usar el directorio actual
        if not presets.get('base_directory'):
            presets['base_directory'] = os.getcwd()
            
        return presets
    except Exception as e:
        print(f"❌ Error cargando presets.json: {e}")
        sys.exit(1)

def check_existing_browser(port=9222):
    """Verificar si ya hay un navegador abierto en el puerto especificado"""
    try:
        response = requests.get(f'http://localhost:{port}/json/version', timeout=2)
        return response.status_code == 200
    except:
        return False

def setup_browser(presets):
    """Configurar y abrir navegador Chrome"""
    global driver, current_task
    
    port = presets.get('browser_port', 9222)
    
    # Verificar si ya hay un navegador abierto
    if check_existing_browser(port):
        print("🔄 Detectado navegador existente, reutilizando sesión...")
        try:
            # Conectar al navegador existente
            chrome_options = Options()
            chrome_options.add_argument(f"--remote-debugging-port={port}")
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{port}")
            
            service = Service(presets['webdriver_path'])
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"⚠️  Error conectando al navegador existente: {e}")
            print("🔄 Creando nueva instancia...")
    
    # Crear nueva instancia del navegador
    print("🌐 Abriendo nueva ventana del navegador...")
    
    chrome_options = Options()
    chrome_options.add_argument(f"--remote-debugging-port={port}")
    chrome_options.add_argument(f"--user-data-dir={presets.get('browser_user_data', './utils/browser_data')}")
    
    if presets.get('headless', False):
        chrome_options.add_argument('--headless')
    
    window_size = presets.get('window_size', [1920, 1080])
    chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    
    # Opciones adicionales para estabilidad
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(presets['webdriver_path'])
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ejecutar script para ocultar que es automatizado
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        print(f"❌ Error iniciando Chrome: {e}")
        print("💡 Asegúrate de que ChromeDriver esté en la ruta correcta")
        sys.exit(1)

def import_task(task_name):
    """Importar dinámicamente la función task desde el archivo especificado"""
    try:
        task_path = f"tasks/{task_name}.py"
        
        if not os.path.exists(task_path):
            print(f"❌ Error: No se encontró la task '{task_name}'")
            print(f"📁 Archivo esperado: {task_path}")
            return None
        
        # Importar el módulo dinámicamente
        spec = importlib.util.spec_from_file_location(f"task_{task_name}", task_path)
        task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_module)
        
        # Verificar que tenga la función task
        if not hasattr(task_module, 'task'):
            print(f"❌ Error: La task '{task_name}' no tiene función task()")
            return None
        
        return task_module.task
    except Exception as e:
        print(f"❌ Error importando task '{task_name}': {e}")
        return None

def main():
    """Función principal"""
    global driver, current_task
    
    print("🚀 Iniciando sistema de automatización web...")
    
    # 1. Verificar argumentos
    if len(sys.argv) != 2:
        print("❌ Error: Debes proporcionar el nombre de una task")
        print("💡 Uso: python main.py <nombre_de_task>")
        sys.exit(1)
    
    task_name = sys.argv[1]
    print(f"📋 Task seleccionada: {task_name}")
    
    # 2. Cargar configuración
    print("⚙️  Cargando configuración...")
    presets = load_presets()
    
    # 3. Importar función de task
    print(f"📦 Importando task '{task_name}'...")
    task_function = import_task(task_name)
    if not task_function:
        sys.exit(1)
    
    # 4. Configurar navegador
    print("🌐 Configurando navegador...")
    driver = setup_browser(presets)
    current_task = task_name
    
    # 5. Preparar objetos de Selenium
    wait = WebDriverWait(driver, presets.get('default_timeout', 10))
    
    # Objetos que se pasarán a la task
    selenium_objects = {
        'driver': driver,
        'wait': wait,
        'By': By,
        'EC': EC,
        'chat': chat  # Incluir función de LLM
    }
    
    # 6. Ejecutar task
    print(f"🎯 Ejecutando task '{task_name}'...")
    try:
        result = task_function(presets, selenium_objects)
        print("✅ Task ejecutada exitosamente")
        if result:
            print(f"📊 Resultado: {result}")
    except Exception as e:
        print(f"❌ Error ejecutando task: {e}")
        import traceback
        traceback.print_exc()
    
    # 7. Mantener navegador abierto
    print("🎪 Navegador mantenido abierto para inspección manual")
    print("💡 Cierra el navegador manualmente cuando hayas terminado")
    
    # Mantener el script vivo para no perder la referencia del driver
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Cerrando sistema...")
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()