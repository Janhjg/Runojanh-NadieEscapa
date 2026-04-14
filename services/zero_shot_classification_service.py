from .traductor_crimenes_service import traductor_datosCrimen

_classifier = None

def get_classifier():
    """Lazy loader para el clasificador de Hugging Face."""
    global _classifier
    if _classifier is None:
        from transformers import pipeline
        _classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _classifier

labels_genéricas_basicas = ["sangriento", "gore", "frío", "calculado", "impulsivo", "triste", "sin sentido", "sádico", "enfermizo", "pasional", "vengativo", "accidental", "misterioso", "ritual", "serial", "masacre", "ejecución", "narco", "cartel", "psicópata", "organizado", "desorganizado", "caótico", "limpio", "sucio", "sobre-ensañamiento"]
labels_tipo_motivo_crimen = ["homicidio", "homicidio múltiple", "familiar", "secuestro", "tortura", "asfixia", "apuñalamiento", "disparo", "estrangulamiento", "golpeamiento", "envenenamiento", "ahogamiento", "incendio", "robo con violencia", "agresión sexual", "doméstico", "pasional", "celos", "discusión", "drogas", "venganza", "accidente", "suicidio disfrazado", "ejecución profesional"]
labels_escena_características = ["escena caótica", "escena limpia", "alta limpieza", "ocultamiento", "fosa", "maletero", "cuerpo abandonado", "sangre en paredes", "huellas ensangrentadas", "trofeos", "grabaciones", "tortura psicológica", "tiro de gracia", "manos atadas", "vendados", "bolsa en cabeza", "cuchillo", "arma de fuego", "arma blanca", "arma improvisada"]
labels_contexto_clasificación = ["violento", "propiedad", "callejero", "barrio", "rural", "urbano", "organizado crime", "narcotráfico", "intrafamiliar", "extraño", "conocido", "víctima menor", "víctima vulnerable", "tragedia evitable", "por nada", "estupidez fatal", "sin alma", "frío como el hielo", "disfrute del sufrimiento", "coleccionista"]

MODELO = "facebook/bart-large-mnli"

def _extraer_top(resultado: dict, top_n: int) -> list[dict]:
    pares = zip(resultado["labels"], resultado["scores"])
    return [{"label": l, "score": round(s, 4)} for l, s in list(pares)[:top_n]]

def construir_clasificacion(datos: dict, VObjetiva=None) -> dict:
    """
    Construye el contexto para HuggingFace y filtra etiquetas según los datos reales
    para evitar alucinaciones (ej: no sugerir arma de fuego si fue un vehículo).
    """
    # 1. Preparación de datos
    if VObjetiva:
        datos = traductor_datosCrimen(datos, VObjetiva)
    else:
        datos = traductor_datosCrimen(datos)

    weapon_desc = (datos.get("Weapon Desc") or "").upper()
    
    # 2. Guardias de Etiquetas (Filtro dinámico para evitar sesgos)
    c_genericas = labels_genéricas_basicas.copy()
    c_motivo    = labels_tipo_motivo_crimen.copy()
    c_escena    = labels_escena_características.copy()

    # Si NO es arma de fuego, eliminamos etiquetas relacionadas con disparos
    firearm_keywords = ["GUN", "FIREARM", "PISTOL", "SHOT", "REVOLVER", "RIFLE"]
    is_firearm = any(k in weapon_desc for k in firearm_keywords)
    
    if not is_firearm:
        to_remove = ["disparo", "tiro de gracia", "arma de fuego"]
        c_motivo = [l for l in c_motivo if l not in to_remove]
        c_escena = [l for l in c_escena if l not in to_remove]
    
    # Si es VEHÍCULO, reforzamos etiquetas de accidente/tragedia si aplica
    if "VEHICLE" in weapon_desc:
        if "accidental" not in c_genericas: c_genericas.append("accidental")

    # 3. Construcción del texto descriptivo
    texto = (
        f'Ocurrido el crimen {datos.get("Crm Cd Desc")} de nivel {datos.get("Part 1-2")}, '
        f'se ha usado el arma {datos.get("Weapon Desc") or "Desconocida"} el dia {datos.get("DATE OCC")}, '
        f'a la hora {datos.get("TIME OCC")}, en {datos.get("AREA NAME")}, '
        f'distrito:{datos.get("Rpt Dist No")}, en un/a {datos.get("Premis Desc")}. '
        f'Informacion de la victima: edad={datos.get("Vict Age")}, sexo={datos.get("Vict Sex")}, '
        f'descendencia={datos.get("Vict Descent")}, '
        f'finalmente el caso será resuelto con {datos.get("Status Desc")}.'
    )

    classifier_instance = get_classifier()

    raw_genericas = classifier_instance(texto, candidate_labels=c_genericas, multi_label=True)
    raw_motivo    = classifier_instance(texto, candidate_labels=c_motivo,    multi_label=True)
    raw_escena    = classifier_instance(texto, candidate_labels=c_escena,    multi_label=True)
    raw_contexto  = classifier_instance(texto, candidate_labels=labels_contexto_clasificación, multi_label=True)

    todas_etiquetas = {
        "labels_genericas":              _extraer_top(raw_genericas, 2),
        "labels_motivo_crimen":          _extraer_top(raw_motivo,    1),
        "labels_escena_caracteristicas": _extraer_top(raw_escena,    3),
        "labels_contexto_clasificacion": _extraer_top(raw_contexto,  2),
    }

    return {
        "etiqueta":         {cat: items[0]["label"] for cat, items in todas_etiquetas.items()},
        "confianza":        {cat: items[0]["score"] for cat, items in todas_etiquetas.items()},
        "texto_construido": texto,
        "todas_etiquetas":  todas_etiquetas,
        "modelo":           MODELO,
    }