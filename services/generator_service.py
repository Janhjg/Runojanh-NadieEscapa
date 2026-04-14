import ollama
from .traductor_crimenes_service import traductor_datosCrimen

def generar_cronica(datos_crimen: dict, prediccion: dict, etiquetas: dict) -> str:
    """
    Genera una cronica de novela negra usando Ollama (gemma4:e2b).
    Integra datos reales, predicciones de ML y múltiples dimensiones narrativas (etiquetas).
    """
    model_name = "gemma4:e2b"
    
    # Extraemos y formateamos las etiquetas para el prompt
    def format_labels(cat_key):
        items = etiquetas.get(cat_key, [])
        return ", ".join([i.get('label') if isinstance(i, dict) else i.label for i in items])

    txt_genericas = format_labels("labels_genericas")
    txt_motivo    = format_labels("labels_motivo_crimen")
    txt_escena    = format_labels("labels_escena_caracteristicas")
    txt_contexto  = format_labels("labels_contexto_clasificacion")

    prompt = f"""
    Eres un aclamado escritor de novela negra, experto en transformar datos policiales fríos en crónicas literarias cargadas de atmósfera, tensión y realismo sucio.
    
    Tu tarea es narrar el siguiente crimen ocurrido en Los Ángeles.
    
    DATOS DEL CRIMEN:
    - Tipo: {datos_crimen.get('Crm_Cd_Desc')}
    - Lugar: {datos_crimen.get('Premis_Desc')} en el área de {datos_crimen.get('AREA_NAME')}
    - Fecha y Hora: {datos_crimen.get('DATE_OCC')} a las {datos_crimen.get('TIME_OCC')}
    - Arma: {datos_crimen.get('Weapon_Desc') or 'Ninguna/Desconocida'}
    - Víctima: Edad {datos_crimen.get('Vict_Age', 'Desconocida')}, Sexo {datos_crimen.get('Vict_Sex', 'Desconocido')}
    
    MATICES NARRATIVOS (Usa estos elementos para tejer la historia):
    - Tonos generales: {txt_genericas}
    - Motivo sugerido: {txt_motivo}
    - Detalles de la escena: {txt_escena}
    - Contexto de clasificación: {txt_contexto}

    PREDICCIÓN POLICIAL (Destino de la investigación): El caso apunta a un resultado de "{prediccion.get('clase_predicha')}" 
    con una confianza del {prediccion.get('confianza', 0)*100:.1f}%.
    
    INSTRUCCIONES NARRATIVAS:
    1. Estilo Noir: Prosa rítmica, cínica, frases cortas y contundentes.
    2. Atmósfera: Los Ángeles nocturno, luces de neón, asfalto mojado, desesperanza urbana.
    3. Integración: Entrelaza de forma orgánica los matices proporcionados ({txt_genericas}, {txt_motivo}, {txt_escena}, {txt_contexto}) para dar profundidad al relato.
    4. Final: Insinúa el destino de "{prediccion.get('clase_predicha')}" en el cierre literario.
    5. Extensión: Aproximadamente 200-250 palabras.
    6. Empieza directamente con la historia, sin preámbulos.
    
    CRÓNICA:
    """

    try:
        response = ollama.chat(model=model_name, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        # Acceso robusto a la respuesta de Ollama
        if hasattr(response, 'message'):
            return response.message.content.strip()
        return response['message']['content'].strip()

    except Exception as e:
        return f"Error en la generación de la crónica (Ollama): {str(e)}"