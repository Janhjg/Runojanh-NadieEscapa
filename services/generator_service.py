import ollama
from .traductor_crimenes_service import traductor_datosCrimen


def generar_cronica(datos_crimen: dict, prediccion: dict, etiquetas: dict) -> str:
    """
    Genera una cronica de novela negra usando Ollama (gemma2:2b).
    Integra datos reales, predicciones de ML y múltiples dimensiones narrativas (etiquetas).
    """
    model_name = "gemma2:2b"

    # Extraemos y formateamos las etiquetas para el prompt
    def format_labels(cat_key):
        items = etiquetas.get(cat_key, [])
        return ", ".join(
            [i.get("label") if isinstance(i, dict) else i.label for i in items]
        )

    txt_genericas = format_labels("labels_genericas")
    txt_motivo = format_labels("labels_motivo_crimen")
    txt_escena = format_labels("labels_escena_caracteristicas")
    txt_contexto = format_labels("labels_contexto_clasificacion")

    # RESTRICCIONES DINÁMICAS (Para evitar alucinaciones de armas)
    weapon_desc = (datos_crimen.get("Weapon Desc") or "").upper()
    firearm_keywords = ["GUN", "FIREARM", "PISTOL", "SHOT", "REVOLVER", "RIFLE"]
    is_firearm = any(k in weapon_desc for k in firearm_keywords)

    forbidden_elements = ""
    if not is_firearm and weapon_desc:
        forbidden_elements = f"ESTÁ PROHIBIDO mencionar armas de fuego, disparos, pólvora o casquillos. El arma fue un {weapon_desc}, enfócate en los detalles de ese objeto."
    elif not weapon_desc:
        forbidden_elements = "No se reportó arma física; no inventes armas de fuego a menos que los matices lo sugieran fuertemente."

    # Enriquecimiento de crímenes secundarios
    crimenes = [datos_crimen.get("Crm Cd Desc")]
    for i in range(2, 5):
        extra = datos_crimen.get(f"Crm Cd {i} Desc")
        if extra:
            crimenes.append(extra)
    txt_crimenes = " y ".join([c for c in crimenes if c])

    # ── TRADUCCIÓN EXPLÍCITA DE DATOS DE VÍCTIMA ──────────────────────────
    # Si no traducimos aquí, Ollama recibe "F", "H", etc. y asume el género incorrecto.
    sexo_raw = datos_crimen.get("Vict Sex", "X")
    sexo_map = {"F": "Femenina", "M": "Masculino", "X": "Desconocido"}
    vict_sex_human = sexo_map.get(sexo_raw, sexo_raw)

    descent_map = {
        "A": "Asiática",
        "B": "Negra",
        "C": "China",
        "D": "Camboyana",
        "F": "Filipina",
        "G": "Guameña",
        "H": "Hispana/Latinoamericana",
        "I": "Indígena americana",
        "J": "Japonesa",
        "K": "Coreana",
        "O": "Otros",
        "P": "Isleña del Pacífico",
        "S": "Samoana",
        "U": "Hawaiana",
        "V": "Vietnamita",
        "W": "Blanca",
        "X": "Desconocida",
        "Z": "Asiático indio",
    }
    vict_descent_human = descent_map.get(
        datos_crimen.get("Vict Descent", "X"),
        datos_crimen.get("Vict Descent", "Desconocida"),
    )
    vict_age = datos_crimen.get("Vict Age", "Desconocida")

    # Ancla de identidad — instrucción explícita para que Ollama no cambie el género
    if sexo_raw == "F":
        identity_anchor = f"OBLIGATORIO: La víctima es una mujer/niña de {vict_age} años. En toda la crónica usa EXCLUSIVAMENTE pronombres femeninos: ella, su, la víctima. NUNCA escribas 'él' para referirte a la víctima."
    elif sexo_raw == "M":
        identity_anchor = f"OBLIGATORIO: La víctima es un hombre/niño de {vict_age} años. En toda la crónica usa EXCLUSIVAMENTE pronombres masculinos: él, su, el hombre. NUNCA escribas 'ella' para referirte a la víctima."
    else:
        identity_anchor = (
            f"La víctima tiene {vict_age} años y su género es desconocido."
        )

    prompt = f"""
    Eres un aclamado escritor de novela negra, experto en transformar datos policiales fríos en crónicas literarias cargadas de atmósfera, tensión y realismo sucio.
    
    Tu tarea es narrar el siguiente crimen ocurrido en Los Ángeles.
    
    DATOS DEL CRIMEN (HECHOS INVIOLABLES - NO los cambies ni inventes):
    - Cargos: {txt_crimenes}
    - Gravedad: {datos_crimen.get('Part 1-2')}
    - Lugar: {datos_crimen.get('Premis Desc')} en el área de {datos_crimen.get('AREA NAME')}
    - Fecha y Hora: {datos_crimen.get('DATE OCC')} a las {datos_crimen.get('TIME OCC')}
    - Arma: {weapon_desc or 'Ninguna/Desconocida'}
    - Víctima: Edad {vict_age}, Sexo {vict_sex_human}, Origen {vict_descent_human}
    
    MATICES NARRATIVOS (Usa estos para dar atmósfera, no para contradecir los hechos):
    - Tonos generales: {txt_genericas}
    - Motivo sugerido: {txt_motivo}
    - Detalles de la escena: {txt_escena}
    - Contexto de clasificación: {txt_contexto}

    PREDICCIÓN POLICIAL: El caso apunta a un resultado de "{prediccion.get('clase_predicha')}" ({prediccion.get('confianza', 0)*100:.1f}%).
    
    INSTRUCCIONES NARRATIVAS (TODAS OBLIGATORIAS):
    1. {identity_anchor}
    2. Estilo Noir: Prosa rítmica, cínica, frases cortas.
    3. Atmósfera: Los Ángeles nocturno, calles del barrio dado.
    4. Los DATOS DEL CRIMEN son hechos reales. No los listes como un informe policial; intégralos en la atmósfera (ej. en lugar de "Simple Assault", descríbelo como una agresión cobarde o un ataque repentino en las sombras).
    5. Final: Narra el destino de la investigación basado en "{prediccion.get('clase_predicha')}". Evita frases técnicas como "el caso es un NO arresto"; en su lugar, describe cómo el sospechoso se desvanece en la impunidad o cómo la justicia finalmente cierra el grillete.
    6. Extensión: 200-250 palabras. Empieza directamente con la historia.
    7. Usar el idioma espanol
    
    PROHIBICIÓN ABSOLUTA:
    {forbidden_elements}
    
    CRÓNICA:
    """

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Acceso robusto a la respuesta de Ollama
        if hasattr(response, "message"):
            return response.message.content.strip()
        return response["message"]["content"].strip()

    except Exception as e:
        return f"Error en la generación de la crónica (Ollama): {str(e)}"
