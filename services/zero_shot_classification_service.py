from .traductor_crimenes_service import traductor_datosCrimen

_classifier = None

def get_classifier():
    """Lazy loader para el clasificador de Hugging Face (BART-Large con Caché Local)."""
    global _classifier
    if _classifier is None:
        from transformers import pipeline
        import torch
        import os
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CACHE_DIR = os.path.join(BASE_DIR, "models", "hf_cache")
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        device = 0 if torch.cuda.is_available() else -1
        
        _classifier = pipeline("zero-shot-classification", 
                               model="facebook/bart-large-mnli",
                               device=device,
                               model_kwargs={"cache_dir": CACHE_DIR})
    return _classifier

MODELO = "facebook/bart-large-mnli"

# ── MAPAS DETERMINISTAS (Ground Truth por datos del CSV) ──────────────────────
# Estas reglas tienen prioridad ABSOLUTA sobre el modelo de IA.

_WEAPON_TO_FISICO = {
    "STRONG-ARM": "agresión física",
    "HANDS": "agresión física",
    "FIST": "agresión física",
    "FEET": "agresión física",
    "BODILY FORCE": "agresión física",
    "VERBAL THREAT": "amenaza verbal",
    "PHYSICAL PRESENCE": "intimidación",
    "UNKNOWN WEAPON": "arma improvisada",
    "ROCK": "arma improvisada",
    "BOTTLE": "arma improvisada",
    "CLUB": "arma improvisada",
    "BAT": "arma improvisada",
    "STICK": "arma improvisada",
    "BLUNT": "arma improvisada",
    "SCISSORS": "arma improvisada",
    "FOLDING KNIFE": "arma blanca",
    "OTHER KNIFE": "arma blanca",
    "KNIFE": "arma blanca",
    "BLADE": "arma blanca",
    "DAGGER": "arma blanca",
    "MACHETE": "arma blanca",
    "SWORD": "arma blanca",
    "OTHER CUTTING": "arma blanca",
    "SEMI-AUTOMATIC PISTOL": "arma de fuego",
    "HAND GUN": "arma de fuego",
    "REVOLVER": "arma de fuego",
    "RIFLE": "arma de fuego",
    "SHOTGUN": "arma de fuego",
    "PISTOL": "arma de fuego",
    "GUN": "arma de fuego",
    "VEHICLE": "vehículo como arma",
    "FIRE": "incendio provocado",
}

_WEAPON_TO_ESTILO = {
    "VERBAL THREAT": "frío",
    "PHYSICAL PRESENCE": "calculado",
    "STRONG-ARM": "impulsivo",
    "KNIFE": "sangrienta",
    "MACHETE": "sobre-ensañamiento",
    "FIREARM": "calculado",
    "GUN": "fría",
    "PISTOL": "calculado",
    "VEHICLE": "caótico",
    "FIRE": "ritual",
}

_CRIME_TO_TEMATICA = {
    "HOMICIDE": "homicidio",
    "MURDER": "homicidio",
    "RAPE": "agresión sexual",
    "SEXUAL": "agresión sexual",
    "ASSAULT": "agresión física",
    "BATTERY": "agresión física",
    "ROBBERY": "robo con violencia",
    "THEFT": "robo",
    "BURGLARY": "robo",
    "KIDNAP": "secuestro",
    "ARSON": "incendio provocado",
    "CHILD": "víctima menor",
    "DOMESTIC": "doméstico",
    "INTIMATE": "intrafamiliar",
    "STALKING": "acoso",
    "VANDALISM": "daño a propiedad",
    "EXTORTION": "extorsión",
    "DRUGS": "narcotráfico",
    "NARCO": "narcotráfico",
    "THREATENING": "amenaza verbal",
}

_CRIME_TO_CONTEXTO = {
    "HOMICIDE": "violento",
    "MURDER": "violento",
    "RAPE": "víctima vulnerable",
    "ROBBERY": "callejero",
    "ASSAULT": "callejero",
    "BATTERY": "callejero",
    "CHILD": "víctima menor",
    "DOMESTIC": "intrafamiliar",
    "INTIMATE": "intrafamiliar",
    "STALKING": "conocido",
    "BURGLARY": "urbano",
    "EXTORTION": "frío como el hielo",
}

def _match_map(value: str, mapping: dict) -> str | None:
    """Busca si alguna clave del mapa aparece en el valor dado."""
    upper = value.upper()
    for k, v in mapping.items():
        if k in upper:
            return v
    return None

def _extraer_top(resultado: dict, top_n: int) -> list[dict]:
    pares = zip(resultado["labels"], resultado["scores"])
    return [{"label": l, "score": round(s, 4)} for l, s in list(pares)[:top_n]]


def construir_clasificacion(datos: dict, VObjetiva=None) -> dict:
    """
    SISTEMA HÍBRIDO:
    1. Primero aplica reglas deterministas basadas en los datos reales (Weapon, Crime).
    2. Solo usa BART para las categorías donde no hay regla determinista (estilo/tono).
    """
    # 1. Preparación de datos
    if VObjetiva:
        datos = traductor_datosCrimen(datos, VObjetiva)
    else:
        datos = traductor_datosCrimen(datos)

    weapon_desc = (datos.get("Weapon Desc") or "").upper()
    crime_desc  = (datos.get("Crm Cd Desc") or "").upper()
    
    vict_age = datos.get("Vict Age")
    try:
        age_num = float(vict_age) if vict_age is not None else 0
    except (ValueError, TypeError):
        age_num = 0

    # 2. ── CLASIFICACIÓN DETERMINISTA (Reglas Duras) ──────────────────────────
    det_fisico   = _match_map(weapon_desc, _WEAPON_TO_FISICO)
    det_tematica = _match_map(crime_desc,  _CRIME_TO_TEMATICA)
    det_contexto = _match_map(crime_desc,  _CRIME_TO_CONTEXTO)
    det_estilo   = _match_map(weapon_desc, _WEAPON_TO_ESTILO)

    # Regla de edad – jamás etiquetar como menor si > 17
    if age_num >= 18:
        if det_tematica in ["víctima menor"]: det_tematica = None
        if det_contexto in ["víctima menor"]: det_contexto = None

    # 3. ── CLASIFICACIÓN CON BART (solo para tags sin regla determinista) ─────
    # Preparamos texto enriquecido para BART
    crimenes = [datos.get("Crm Cd Desc")]
    for i in range(2, 5):
        extra = datos.get(f"Crm Cd {i} Desc")
        if extra: crimenes.append(extra)
    txt_crimenes = " y ".join([c for c in crimenes if c])
    
    texto = (
        f'Crimen: {txt_crimenes}. '
        f'Arma utilizada: {datos.get("Weapon Desc") or "Desconocida"}. '
        f'Lugar: {datos.get("Premis Desc")} en {datos.get("AREA NAME")}. '
        f'Víctima: {datos.get("Vict Age")} años, sexo {datos.get("Vict Sex")}. '
        f'Severidad del crimen: {datos.get("Part 1-2")}.'
    )

    # Solo llamar a BART para lo que no tenemos en la regla dura
    classifier_instance = get_classifier()
    
    # Estilo – siempre BART (subjetivo)
    labels_estilo = ["frío y calculado", "impulsivo y violento", "metódico", "caótico", "misterioso", "psicópata", "organizado", "sobre-ensañamiento"]
    raw_estilo = classifier_instance(texto, candidate_labels=labels_estilo, multi_label=True)
    
    # Para tematica/fisico/contexto: si tenemos regla dura, no llamamos a BART
    if not det_tematica:
        labels_tematica = ["homicidio", "robo con violencia", "agresión física", "agresión sexual", "doméstico", "narcotráfico", "extorsión", "secuestro", "acoso"]
        raw_tem = classifier_instance(texto, candidate_labels=labels_tematica, multi_label=False)
        det_tematica = raw_tem["labels"][0]

    if not det_fisico:
        labels_fisico = ["agresión física", "arma de fuego", "arma blanca", "arma improvisada", "amenaza verbal", "vehículo como arma"]
        raw_fis = classifier_instance(texto, candidate_labels=labels_fisico, multi_label=False)
        det_fisico = raw_fis["labels"][0]

    if not det_contexto:
        labels_contexto = ["callejero", "intrafamiliar", "urbano", "victima vulnerable", "conocido", "extraño"]
        raw_ctx = classifier_instance(texto, candidate_labels=labels_contexto, multi_label=False)
        det_contexto = raw_ctx["labels"][0]

    if not det_estilo:
        det_estilo = _extraer_top(raw_estilo, 1)[0]["label"]

    # 4. Armado del resultado final
    todas_etiquetas = {
        "labels_genericas":              [{"label": det_estilo,   "score": 1.0}],
        "labels_motivo_crimen":          [{"label": det_tematica, "score": 1.0}],
        "labels_escena_caracteristicas": [{"label": det_fisico,   "score": 1.0}],
        "labels_contexto_clasificacion": [{"label": det_contexto, "score": 1.0}],
    }

    return {
        "etiqueta":         {cat: items[0]["label"] for cat, items in todas_etiquetas.items()},
        "confianza":        {cat: items[0]["score"] for cat, items in todas_etiquetas.items()},
        "texto_construido": texto,
        "todas_etiquetas":  todas_etiquetas,
        "modelo":           MODELO,
    }