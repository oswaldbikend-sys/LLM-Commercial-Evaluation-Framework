import os
import json
import google.generativeai as genai
import PIL.Image

# Configuración de API
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "TU_API_KEY_DE_GEMINI_AQUI")
genai.configure(api_key=GOOGLE_API_KEY)

def auditar_imagen(ruta_imagen, adn_visual_prompt):
    """
    Simula la auditoría de una imagen utilizando Gemini Multimodal.
    Verifica el cumplimiento estricto del ADN visual provisto.
    """
    try:
        if not os.path.exists(ruta_imagen):
            return json.dumps({
                "status": "FAIL",
                "justification": f"Error: No se encontró la imagen en {ruta_imagen}"
            })

        img = PIL.Image.open(ruta_imagen)
        
        # Usamos gemini-2.5-pro, ya que es el modelo más reciente con soporte para Visión
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt_evaluacion = f"""
        Actúa como un Auditor de Calidad Multimodal experto en continuidad y ADN Visual de Marca.
        Evalúa la imagen proporcionada estrictamente contra las siguientes reglas:
        
        [REGLAS DE ADN VISUAL]
        {adn_visual_prompt}
        
        Devuelve tu respuesta ÚNICAMENTE en formato JSON válido con esta estructura exacta:
        {{
            "status": "Escribe 'PASS' si cumple todas las reglas, o 'FAIL' si rompe al menos una regla",
            "justification": "Escribe una justificación analítica en inglés de tu veredicto"
        }}
        """
        
        response = model.generate_content(
            [prompt_evaluacion, img],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        return response.text.strip()
        
    except Exception as e:
        return json.dumps({
            "status": "ERROR",
            "justification": str(e)
        })

if __name__ == "__main__":
    # Simulación de prueba rápida si se ejecuta directamente
    print("Módulo Visual QA Auditor inicializado correctamente.")
    print("Para probarlo, llama a la función auditar_imagen(ruta_imagen, adn_visual_prompt).")
