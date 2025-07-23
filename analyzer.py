import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_cv(cv_text, job_description):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    Eres un analista de recursos humanos experto. Analiza el CV del candidato en función de la oferta de trabajo provista.

    Job Description:
    {job_description}

    CV:
    {cv_text}

     Instrucciones para el análisis:
    1.  **Idioma:** Realiza todo el análisis en español.
    2.  **Análisis de coincidencias:** Identifica y lista las habilidades y la experiencia clave del CV que coinciden directamente con los requisitos de la oferta para un "Junior Project Manager".
    3.  **Áreas de mejora:** Señala las áreas en las que la experiencia del candidato parece ser deficiente o no coincide con los requisitos de la oferta.
    4.  **Resumen de idoneidad:** Ofrece un resumen conciso de la idoneidad del candidato para el rol, basándote en tu análisis.
    5.  **Score de fit:** Asigna un puntaje de 0.0 a 10.0 que indique qué tan bien se ajusta el candidato al puesto, donde:
        - 0.0-2.0: No calificado para el puesto
        - 2.1-4.0: Poco calificado, necesita mucha capacitación
        - 4.1-6.0: Calificación moderada, puede crecer en el rol
        - 6.1-8.0: Bien calificado, buen ajuste al puesto
        - 8.1-10.0: Excelente calificación, ajuste perfecto
    6.  **Formato de salida:** Retorna el análisis exclusivamente en formato JSON. No incluyas ningún texto adicional antes o después del JSON.

    Formato JSON requerido:
    ```json
    {{
        "nombre_candidato": "Nombre completo del candidato (si está disponible en el CV)",
        "email": "Email del candidato (si está disponible)",
        "puesto_solicitado": "Junior Project Manager",
        "score_fit": 7.5,
        "nivel_experiencia": "Junior",
        "tiempo_experiencia": "2 años",
        "analisis_match": {{
            "habilidades_coincidentes": ["habilidad 1", "habilidad 2"],
            "experiencia_coincidente": ["experiencia 1", "experiencia 2"]
        }},
        "puntos_de_mejora": [
            "Área de mejora 1",
            "Área de mejora 2"
        ],
        "resumen_idoneidad": "Resumen conciso sobre la idoneidad del candidato para el puesto.",
        "recomendacion": "Recomendado para entrevista",
        "riesgos": ["riesgo 1", "riesgo 2"],
        "fortalezas": ["fortaleza 1", "fortaleza 2"]
    }}
    """
    response = model.generate_content(prompt)
    return response.text
