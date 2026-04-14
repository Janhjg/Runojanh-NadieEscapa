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

# ✅ Remap snake_case (Pydantic) → nombres reales del CSV
def _normalizar_claves(datos: dict) -> dict:
    return {
        "Part 1-2":    datos.get("Part_1_2"),
        "Crm Cd Desc": datos.get("Crm_Cd_Desc"),
        "Weapon Desc": datos.get("Weapon_Desc"),
        "DATE OCC":    datos.get("DATE_OCC"),
        "TIME OCC":    datos.get("TIME_OCC"),
        "AREA NAME":   datos.get("AREA_NAME"),
        "Rpt Dist No": datos.get("Rpt_Dist_No"),
        "Premis Desc": datos.get("Premis_Desc"),
        "Vict Age":    datos.get("Vict_Age"),
        "Vict Sex":    datos.get("Vict_Sex"),
        "Vict Descent":datos.get("Vict_Descent"),
        "Status Desc": datos.get("Status_Desc"),
    }

def _extraer_top(resultado: dict, top_n: int) -> list[dict]:
    pares = zip(resultado["labels"], resultado["scores"])
    return [{"label": l, "score": round(s, 4)} for l, s in list(pares)[:top_n]]


def construir_clasificacion(datos: dict, VObjetiva=None) -> dict:
    # ✅ Normalizar antes de pasarle al traductor
    datos = _normalizar_claves(datos)

    if VObjetiva:
        datos = traductor_datosCrimen(datos, VObjetiva)
    else:
        datos = traductor_datosCrimen(datos)

    texto = (
        f'Ocurrido el crimen {datos["Crm Cd Desc"]} de nivel {datos["Part 1-2"]}, '
        f'se ha usado el arma {datos["Weapon Desc"]} el dia {datos["DATE OCC"]}, '
        f'a la hora {datos["TIME OCC"]}, en {datos["AREA NAME"]}, '
        f'distrito:{datos["Rpt Dist No"]}, en un/a {datos["Premis Desc"]}. '
        f'Informacion de la victima: edad={datos["Vict Age"]}, sexo={datos["Vict Sex"]}, '
        f'descendencia={datos["Vict Descent"]}, '
        f'finalmente el caso será resuelto con {datos["Status Desc"]}.'
    )

    classifier_instance = get_classifier()

    raw_genericas = classifier_instance(texto, candidate_labels=labels_genéricas_basicas,     multi_label=True)
    raw_motivo    = classifier_instance(texto, candidate_labels=labels_tipo_motivo_crimen,     multi_label=True)
    raw_escena    = classifier_instance(texto, candidate_labels=labels_escena_características, multi_label=True)
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