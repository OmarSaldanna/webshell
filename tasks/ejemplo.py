#!/usr/bin/env python3

import time

def task(presets, selenium_objects):
    """
    Task de ejemplo que demuestra el uso del sistema
    
    Args:
        presets (dict): Configuración del sistema desde presets.json
        selenium_objects (dict): Objetos de Selenium y utilidades
            - driver: WebDriver de Selenium
            - wait: WebDriverWait configurado
            - By: Selector de elementos
            - EC: Expected Conditions
            - chat: Función para hacer prompts a LLM
    
    Returns:
        dict: Resultado de la automatización
    """
    
    # Extraer objetos de Selenium
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    By = selenium_objects['By']
    EC = selenium_objects['EC']
    chat = selenium_objects['chat']
    
    print("🎯 Iniciando task de ejemplo...")
    
    try:
        # 1. Navegar a una página web
        print("🌐 Navegando a Google...")
        driver.get("https://www.google.com")
        
        # 2. Esperar a que cargue la página
        print("⏳ Esperando que cargue la página...")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        
        # 3. Usar LLM para generar un término de búsqueda
        print("🤖 Consultando LLM para término de búsqueda...")
        llm_response = chat(
            presets['openai_model'], 
            "Dame un término de búsqueda interesante sobre tecnología. Responde con JSON: {'search_term': 'tu_termino_aqui', 'reason': 'por_que_elegiste_este_termino'}"
        )
        
        if llm_response['success']:
            search_term = llm_response['data'].get('search_term', 'Selenium automation')
            reason = llm_response['data'].get('reason', 'Término por defecto')
            print(f"💡 LLM sugiere buscar: '{search_term}'")
            print(f"📝 Razón: {reason}")
        else:
            search_term = "Selenium Python automation"
            print(f"⚠️  Error en LLM, usando término por defecto: {search_term}")
        
        # 4. Realizar búsqueda
        print(f"🔍 Realizando búsqueda: {search_term}")
        search_box.send_keys(search_term)
        search_box.submit()
        
        # 5. Esperar resultados
        print("📊 Esperando resultados de búsqueda...")
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        
        # 6. Obtener algunos resultados
        print("📋 Obteniendo primeros resultados...")
        results = driver.find_elements(By.CSS_SELECTOR, "h3")[:3]
        
        result_titles = []
        for i, result in enumerate(results, 1):
            title = result.text
            result_titles.append(title)
            print(f"   {i}. {title}")
        
        # 7. Usar LLM para analizar resultados
        print("🧠 Analizando resultados con LLM...")
        analysis_prompt = f"""
        Analiza estos títulos de resultados de búsqueda para "{search_term}":
        {chr(10).join([f"{i+1}. {title}" for i, title in enumerate(result_titles)])}
        
        Responde con JSON: {{
            "summary": "resumen_breve_de_los_resultados",
            "most_relevant": "numero_del_resultado_mas_relevante",
            "insights": ["insight1", "insight2", "insight3"]
        }}
        """
        
        analysis = chat(presets['openai_model'], analysis_prompt)
        
        if analysis['success']:
            print("📈 Análisis LLM:")
            print(f"   📄 Resumen: {analysis['data'].get('summary', 'N/A')}")
            print(f"   🎯 Más relevante: Resultado #{analysis['data'].get('most_relevant', 'N/A')}")
            print("   💡 Insights:")
            for insight in analysis['data'].get('insights', []):
                print(f"      • {insight}")
        
        # 8. Tomar screenshot
        # print("📸 Tomando screenshot...")
        # screenshot_path = f"utils/screenshot_ejemplo_{int(time.time())}.png"
        # driver.save_screenshot(screenshot_path)
        # print(f"💾 Screenshot guardado: {screenshot_path}")
        
        # 9. Resultado final
        result = {
            "success": True,
            "search_term": search_term,
            "results_found": len(result_titles),
            "result_titles": result_titles,
            "llm_analysis": analysis['data'] if analysis['success'] else None,
            "screenshot": screenshot_path,
            "page_title": driver.title,
            "current_url": driver.current_url
        }
        
        print("🎉 Task completada exitosamente!")
        return result
        
    except Exception as e:
        print(f"❌ Error en task: {e}")
        return {
            "success": False,
            "error": str(e),
            "page_title": driver.title if driver else "N/A",
            "current_url": driver.current_url if driver else "N/A"
        }

# Función de prueba independiente
def test_task():
    """Función para probar la task de forma independiente"""
    print("🧪 Ejecutando test de la task ejemplo...")
    
    # Mock de presets y selenium_objects para testing
    mock_presets = {
        "openai_model": "gpt-4o-mini",
        "default_timeout": 10
    }
    
    mock_selenium = {
        "chat": lambda model, prompt: {
            "success": True,
            "data": {
                "search_term": "Python Selenium testing",
                "reason": "Es relevante para automatización web"
            }
        }
    }
    
    print("✅ Mock test completado")

if __name__ == "__main__":
    test_task()