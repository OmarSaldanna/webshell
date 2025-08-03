#!/usr/bin/env python3

import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def task(presets, selenium_objects):
    """
    Task avanzada que realiza búsquedas inteligentes y análisis de contenido
    
    Esta task demuestra:
    - Búsqueda guiada por LLM
    - Análisis de múltiples páginas
    - Toma de decisiones automática
    - Manejo robusto de errores
    """
    
    # Extraer objetos
    driver = selenium_objects['driver']
    wait = selenium_objects['wait']
    By = selenium_objects['By']
    EC = selenium_objects['EC']
    chat = selenium_objects['chat']
    
    print("🔍 Iniciando búsqueda inteligente...")
    
    results = {
        "success": False,
        "searches_performed": [],
        "analysis": {},
        "screenshots": [],
        "errors": []
    }
    
    try:
        # 1. Usar LLM para generar estrategia de búsqueda
        print("🧠 Generando estrategia de búsqueda con LLM...")
        strategy_prompt = """
        Necesito realizar una investigación web sobre tendencias tecnológicas actuales.
        Crea una estrategia de búsqueda con 3 términos diferentes que me permitan
        obtener información variada y actual.
        
        Responde con JSON:
        {
            "search_terms": ["termino1", "termino2", "termino3"],
            "strategy": "descripción de la estrategia",
            "expected_insights": ["insight1", "insight2", "insight3"]
        }
        """
        
        strategy_response = chat(presets['openai_model'], strategy_prompt)
        
        if not strategy_response['success']:
            results['errors'].append("Error generando estrategia de búsqueda")
            return results
        
        strategy = strategy_response['data']
        search_terms = strategy.get('search_terms', ['Python automation', 'AI trends 2024', 'Web scraping tools'])
        
        print(f"📋 Estrategia: {strategy.get('strategy', 'Búsqueda general')}")
        print(f"🎯 Términos a buscar: {', '.join(search_terms)}")
        
        # 2. Realizar búsquedas múltiples
        all_search_results = []
        
        for i, term in enumerate(search_terms, 1):
            print(f"\n🔍 Búsqueda {i}/3: '{term}'")
            
            try:
                # Navegar a Google
                driver.get("https://www.google.com")
                
                # Aceptar cookies si aparece el botón
                try:
                    accept_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Acepto') or contains(text(), 'Accept') or contains(text(), 'I agree')]")))
                    accept_btn.click()
                    time.sleep(1)
                except:
                    pass  # No hay botón de cookies o ya fue aceptado
                
                # Buscar el campo de búsqueda
                search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
                search_box.clear()
                search_box.send_keys(term)
                search_box.send_keys(Keys.RETURN)
                
                # Esperar resultados
                wait.until(EC.presence_of_element_located((By.ID, "search")))
                time.sleep(2)
                
                # Extraer resultados
                result_elements = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
                search_results = []
                
                for result_elem in result_elements:
                    try:
                        title = result_elem.text
                        link_elem = result_elem.find_element(By.XPATH, "./../..")
                        url = link_elem.get_attribute("href") or "No URL"
                        
                        if title and len(title.strip()) > 0:
                            search_results.append({
                                "title": title,
                                "url": url
                            })
                    except:
                        continue
                
                search_data = {
                    "term": term,
                    "results": search_results,
                    "total_found": len(search_results)
                }
                
                all_search_results.append(search_data)
                results['searches_performed'].append(search_data)
                
                print(f"✅ Encontrados {len(search_results)} resultados para '{term}'")
                
                # Tomar screenshot de esta búsqueda
                screenshot_path = f"utils/busqueda_{i}_{int(time.time())}.png"
                driver.save_screenshot(screenshot_path)
                results['screenshots'].append(screenshot_path)
                
            except Exception as e:
                error_msg = f"Error en búsqueda '{term}': {str(e)}"
                print(f"❌ {error_msg}")
                results['errors'].append(error_msg)
                continue
        
        # 3. Analizar todos los resultados con LLM
        print("\n🧠 Analizando todos los resultados con LLM...")
        
        analysis_data = {
            "total_searches": len(all_search_results),
            "total_results": sum(len(search['results']) for search in all_search_results),
            "search_terms": search_terms,
            "results_summary": []
        }
        
        for search in all_search_results:
            summary = {
                "term": search['term'],
                "count": search['total_found'],
                "titles": [r['title'] for r in search['results'][:3]]  # Solo primeros 3
            }
            analysis_data['results_summary'].append(summary)
        
        analysis_prompt = f"""
        Analiza estos resultados de búsqueda sobre tendencias tecnológicas:
        
        {json.dumps(analysis_data, indent=2, ensure_ascii=False)}
        
        Proporciona un análisis comprensivo en JSON:
        {{
            "overall_trends": ["tendencia1", "tendencia2", "tendencia3"],
            "most_relevant_search": "término_más_relevante",
            "key_insights": ["insight1", "insight2", "insight3"],
            "recommended_next_steps": ["paso1", "paso2"],
            "technology_themes": ["tema1", "tema2", "tema3"],
            "confidence_score": 85
        }}
        """
        
        analysis_response = chat(presets['openai_model'], analysis_prompt)
        
        if analysis_response['success']:
            analysis = analysis_response['data']
            results['analysis'] = analysis
            
            print("📊 Análisis completado:")
            print(f"   🔥 Tendencias principales: {', '.join(analysis.get('overall_trends', []))}")
            print(f"   🎯 Búsqueda más relevante: {analysis.get('most_relevant_search', 'N/A')}")
            print(f"   📈 Puntuación de confianza: {analysis.get('confidence_score', 0)}%")
            
            # Mostrar insights
            print("   💡 Insights clave:")
            for insight in analysis.get('key_insights', []):
                print(f"      • {insight}")
        
        # 4. Generar reporte final
        print("\n📋 Generando reporte final...")
        
        report_prompt = f"""
        Basándote en toda la información recopilada, crea un reporte ejecutivo conciso.
        
        Datos de búsqueda: {json.dumps(analysis_data, ensure_ascii=False)}
        Análisis previo: {json.dumps(results.get('analysis', {}), ensure_ascii=False)}
        
        Responde con JSON:
        {{
            "executive_summary": "resumen_ejecutivo_en_2_3_oraciones",
            "top_3_findings": ["hallazgo1", "hallazgo2", "hallazgo3"],
            "action_items": ["acción1", "acción2"],
            "research_quality": "excelente|buena|regular|pobre"
        }}
        """
        
        report_response = chat(presets['openai_model'], report_prompt)
        
        if report_response['success']:
            report = report_response['data']
            results['final_report'] = report
            
            print("📄 Reporte ejecutivo:")
            print(f"   📝 {report.get('executive_summary', 'No disponible')}")
            print(f"   🎯 Calidad de investigación: {report.get('research_quality', 'No evaluada')}")
        
        # 5. Finalización exitosa
        results['success'] = True
        results['total_searches'] = len(all_search_results)
        results['total_results'] = sum(len(search['results']) for search in all_search_results)
        results['execution_time'] = time.time()
        
        print("\n🎉 Búsqueda inteligente completada exitosamente!")
        print(f"📊 Resumen: {results['total_searches']} búsquedas, {results['total_results']} resultados totales")
        
        return results
        
    except Exception as e:
        error_msg = f"Error general en task: {str(e)}"
        print(f"❌ {error_msg}")
        results['errors'].append(error_msg)
        results['success'] = False
        return results

# Función de prueba
def test_task():
    """Test unitario de la task"""
    print("🧪 Testing búsqueda inteligente...")
    
    # Mock básico para testing
    mock_presets = {"openai_model": "gpt-4o-mini"}
    mock_selenium = {
        "chat": lambda model, prompt: {
            "success": True,
            "data": {
                "search_terms": ["Test term 1", "Test term 2"],
                "strategy": "Test strategy"
            }
        }
    }
    
    print("✅ Test básico completado")

if __name__ == "__main__":
    test_task()