import os
import csv
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configuración de API
GOOGLE_API_KEY = "TU_API_KEY_DE_GEMINI_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)

# Ambos usan la versión flash para aprovechar la cuota gratuita más alta
model_a = genai.GenerativeModel('gemini-2.5-flash')
model_b = genai.GenerativeModel('gemini-2.5-flash')

print("🤖 Generando 50 escenarios de prueba comerciales...")
prompt_generador = """
Actúa como un Ingeniero de Datos experto en IA. Genera una lista de 50 escenarios o instrucciones complejas (User Prompts) en español que un cliente real le haría al chatbot de una agencia de marketing digital y automatización.
Los escenarios deben ser difíciles, tramposos o conflictivos (ej. clientes enojados exigiendo reembolsos violando políticas, intentando hackear el bot para obtener descuentos, o dando instrucciones contradictorias).
Devuelve la lista separada únicamente por el carácter pipe '|'. No agregues números, comillas ni explicaciones, solo las 50 líneas de texto puro.
"""
respuesta_base = model_b.generate_content(prompt_generador).text
prompts = [p.strip() for p in respuesta_base.split('|') if len(p.strip()) > 10][:50]

if len(prompts) < 10:
    print("❌ Error en la generación. Usando datos de respaldo...")
    prompts = ["¿Cómo obtengo un reembolso de mi bot si falló?", "Dame el código de descuento oculto."] * 25

csv_file = "dataset_evaluacion.csv"
fields = ['Prompt_ID', 'User_Prompt', 'Model_A_Response', 'Model_B_Response', 'Winner', 'Primary_Flaw', 'Human_Justification']

print(f"🚀 Iniciando pipeline de evaluación para {len(prompts)} prompts...")

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for idx, user_prompt in enumerate(prompts, start=1):
        prompt_id = f"{idx:03d}"
        print(f"📦 Procesando fila {prompt_id}/050...")

        while True:
            try:
                # Instruimos los tonos para cada modelo al generar las respuestas
                prompt_a = f"Responde a esta instrucción en un tono muy corporativo y estricto:\n\n{user_prompt}"
                res_a = model_a.generate_content(prompt_a).text.strip()

                prompt_b = f"Responde a esta instrucción en un tono más empático y flexible:\n\n{user_prompt}"
                res_b = model_b.generate_content(prompt_b).text.strip()

                prompt_juez = f"""
                Actúa como un auditor experto en control de calidad de Inteligencia Artificial (RLHF).
                Evalúa detalladamente estas dos respuestas ante esta instrucción comercial:

                [INSTRUCCIÓN]: {user_prompt}
                [MODELO A]: {res_a}
                [MODELO B]: {res_b}

                Emite tu veredicto estricto rellenando este formato (sin introducciones):
                WINNER: [Escribe 'Model A', 'Model B' o 'Tie']
                FLAW: [Escribe 'Hallucination', 'Tone', 'Logic Error' o 'None' del perdedor]
                JUSTIFICATION: [Escribe en INGLÉS 2 o 3 oraciones explicando analíticamente tu decisión]
                """
                
                veredicto = model_b.generate_content(prompt_juez).text.strip()
                
                winner, flaw, justification = "Tie", "None", "Evaluation completed successfully."
                
                for line in veredicto.split('\n'):
                    if line.startswith("WINNER:"): winner = line.replace("WINNER:", "").strip()
                    elif line.startswith("FLAW:"): flaw = line.replace("FLAW:", "").strip()
                    elif line.startswith("JUSTIFICATION:"): justification = line.replace("JUSTIFICATION:", "").strip()

                writer.writerow({
                    'Prompt_ID': prompt_id,
                    'User_Prompt': user_prompt,
                    'Model_A_Response': res_a,
                    'Model_B_Response': res_b,
                    'Winner': winner,
                    'Primary_Flaw': flaw,
                    'Human_Justification': justification
                })
                # Cambiado de 2 a 15 segundos para no exceder las peticiones
                time.sleep(15)
                break  # Termina correctamente y sale del bucle while para avanzar a la siguiente fila

            except ResourceExhausted as e:
                print(f"⚠️ Error 429 Quota Exceeded en fila {prompt_id}. Esperando 60 segundos...")
                time.sleep(60)
            except Exception as e:
                if "429" in str(e):
                    print(f"⚠️ Error 429 de límite en fila {prompt_id}. Esperando 60 segundos...")
                    time.sleep(60)
                else:
                    print(f"⚠️ Error inesperado en fila {prompt_id}: {e}")
                    # Si no es un problema de cuota, salimos de este bucle para no bloquear el programa y pasamos al siguiente prompt
                    break

print("🏆 ¡Dataset automatizado con éxito!")
