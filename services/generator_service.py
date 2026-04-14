import ollama
from .traductor_crimenes_service import traductor_datosCrimen

def generar_cronica(datos_crimen: dict, prediccion: dict, etiquetas: dict) -> str:
    """
    Genera una cronica de novela negra usando Ollama (gemma4:e2b).
    Integra datos reales, predicciones de ML y múltiples dimensiones narrativas (etiquetas).
    """
    model_name = "gemma2:2b"
    
    # Extraemos y formateamos las etiquetas para el prompt
    def format_labels(cat_key):
        items = etiquetas.get(cat_key, [])
        return ", ".join([i.get('label') if isinstance(i, dict) else i.label for i in items])

    txt_genericas = format_labels("labels_genericas")
    txt_motivo    = format_labels("labels_motivo_crimen")
    txt_escena    = format_labels("labels_escena_caracteristicas")
    txt_contexto  = format_labels("labels_contexto_clasificacion")

    # RESTRICCIONES DINÁMICAS (Para evitar alucinaciones)
    weapon_desc = (datos_crimen.get('Weapon Desc') or '').upper()
    firearm_keywords = ["GUN", "FIREARM", "PISTOL", "SHOT", "REVOLVER", "RIFLE"]
    is_firearm = any(k in weapon_desc for k in firearm_keywords)
    
    forbidden_elements = ""
    if not is_firearm and weapon_desc:
        forbidden_elements = f"ESTÁ PROHIBIDO mencionar armas de fuego, disparos, pólvora o casquillos. El arma fue un {weapon_desc}, enfócate en los detalles de ese objeto."
    elif not weapon_desc:
         forbidden_elements = "No se reportó arma física; no inventes armas de fuego a menos que los matices lo sugieran fuertemente."

    prompt = f"""
    Eres un aclamado escritor de novela negra, experto en transformar datos policiales fríos en crónicas literarias cargadas de atmósfera, tensión y realismo sucio.
    
    Tu tarea es narrar el siguiente crimen ocurrido en Los Ángeles.
    
    DATOS DEL CRIMEN:
    - Tipo: {datos_crimen.get('Crm Cd Desc')}
    - Lugar: {datos_crimen.get('Premis Desc')} en el área de {datos_crimen.get('AREA NAME')}
    - Fecha y Hora: {datos_crimen.get('DATE OCC')} a las {datos_crimen.get('TIME OCC')}
    - Arma: {weapon_desc or 'Ninguna/Desconocida'}
    - Víctima: Edad {datos_crimen.get('Vict Age', 'Desconocida')}, Sexo {datos_crimen.get('Vict Sex', 'Desconocido')}
    
    MATICES NARRATIVOS (Usa estos elementos para tejer la historia):
    - Tonos generales: {txt_genericas}
    - Motivo sugerido: {txt_motivo}
    - Detalles de la escena: {txt_escena}
    - Contexto de clasificación: {txt_contexto}

    PREDICCIÓN POLICIAL: El caso apunta a un resultado de "{prediccion.get('clase_predicha')}" ({prediccion.get('confianza', 0)*100:.1f}%).
    
    INSTRUCCIONES NARRATIVAS (OBLIGATORIAS):
    1. {forbidden_elements}
    2. Estilo Noir: Prosa rítmica, cínica, frases cortas.
    3. Atmósfera: Los Ángeles nocturno, luces de neón, asfalto mojado.
    4. Integración: Entrelaza orgánicamente los matices ({txt_genericas}, {txt_motivo}, {txt_escena}) respetando siempre los DATOS DEL CRIMEN.
    5. Final: Insinúa el destino de "{prediccion.get('clase_predicha')}".
    6. Empieza directamente con la historia.
    
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