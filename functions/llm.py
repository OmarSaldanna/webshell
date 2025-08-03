import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def chat(modelo: str, prompt: str) -> dict:
    """
    Función para hacer prompt a un modelo de OpenAI
    
    Args:
        modelo (str): Modelo de OpenAI a usar (ej: 'gpt-4o-mini')
        prompt (str): Prompt a enviar al modelo
        
    Returns:
        dict: Respuesta del modelo en formato JSON
    """
    try:
        # Inicializar cliente de OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Realizar la consulta
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Siempre responde con un objeto JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extraer el contenido de la respuesta
        content = response.choices[0].message.content.strip()
        
        # Intentar parsear como JSON
        try:
            json_response = json.loads(content)
            return {
                "success": True,
                "data": json_response,
                "raw_content": content,
                "model_used": modelo,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
        except json.JSONDecodeError:
            # Si no es JSON válido, intentar extraer JSON del contenido
            # Buscar bloques de código JSON
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                try:
                    json_response = json.loads(json_match.group(1))
                    return {
                        "success": True,
                        "data": json_response,
                        "raw_content": content,
                        "model_used": modelo,
                        "tokens_used": response.usage.total_tokens if response.usage else 0
                    }
                except json.JSONDecodeError:
                    pass
            
            # Si aún no es JSON, devolver como texto plano pero marcando el error
            return {
                "success": False,
                "error": "La respuesta no es JSON válido",
                "raw_content": content,
                "model_used": modelo,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "raw_content": "",
            "model_used": modelo,
            "tokens_used": 0
        }

# Función auxiliar para debugging
def test_chat():
    """Función de prueba para verificar que la integración funciona"""
    test_prompt = "Dame un objeto JSON con información sobre el clima, incluyendo temperatura, humedad y descripción."
    result = chat("gpt-4o-mini", test_prompt)
    print("🧪 Resultado del test:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

if __name__ == "__main__":
    test_chat()