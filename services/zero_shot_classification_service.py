from .traductor_crimenes_service import traductor_datosCrimen

_classifier = None

def get_classifier():
    """Lazy loader para el clasificador de Hugging Face (BART-Large con Caché Local)."""
    global _classifier
    if _classifier is None:
        from transformers import pipeline
        import torch
        import os
        
        # ── Configuración de Caché Local ─────────────────────────────
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CACHE_DIR = os.path.join(BASE_DIR, "models", "hf_cache")
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        # Auto-detección de GPU para máxima velocidad si está disponible
        device = 0 if torch.cuda.is_available() else -1
        
        _classifier = pipeline("zero-shot-classification", 
                               model="facebook/bart-large-mnli",
                               device=device,
                               model_kwargs={"cache_dir": CACHE_DIR})
    return _classifier

# Etiquetas optimizadas para reducir latencia
labels_estilo_escena = ["sangriento", "frío", "calculado", "impulsivo", "triste", "misterioso", "ritual", "psicópata", "organizado", "caótico", "limpio", "sobre-ensañamiento"]
labels_tematica_contexto = ["homicidio", "familiar", "secuestro", "tortura", "robo con violencia", "agresión sexual", "doméstico", "venganza", "accidente", "ejecución profesional", "narcotráfico", "intrafamiliar", "víctima menor"]
labels_detalles_fisicos = ["escena limpia", "ocultamiento", "cuerpo abandonado", "huellas", "tiro de gracia", "manos atadas", "arma de fuego", "arma blanca", "arma improvisada"]
labels_contexto_clasificacion = ["violento", "callejero", "urbano", "narcotráfico", "intrafamiliar", "extraño", "conocido", "víctima menor", "víctima vulnerable", "tragedia evitable", "sin alma", "frío como el hielo"]

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
    c_estilo  = labels_estilo_escena.copy()
    c_tematica = labels_tematica_contexto.copy()
    c_fisicos  = labels_detalles_fisicos.copy()
    c_contexto = labels_contexto_clasificacion.copy()

    # Si NO es arma de fuego, eliminamos etiquetas relacionadas con disparos
    firearm_keywords = ["GUN", "FIREARM", "PISTOL", "SHOT", "REVOLVER", "RIFLE"]
    is_firearm = any(k in weapon_desc for k in firearm_keywords)
    
    if not is_firearm:
        to_remove = ["disparo", "tiro de gracia", "arma de fuego"]
        c_tematica = [l for l in c_tematica if l not in to_remove]
        c_fisicos  = [l for l in c_fisicos  if l not in to_remove]
    
    # Si es VEHÍCULO, reforzamos etiquetas de accidente
    if "VEHICLE" in weapon_desc:
        if "accidente" not in c_tematica: c_tematica.append("accidente")

    # 3. Construcción del texto descriptivo (Enriquecido con crímenes secundarios)
    crimenes = [datos.get("Crm Cd Desc")]
    for i in range(2, 5):
        extra = datos.get(f"Crm Cd {i} Desc")
        if extra: crimenes.append(extra)
    
    txt_crimenes = " y ".join([c for c in crimenes if c])

    texto = (
        f'Ocurrido el crimen {txt_crimenes} de nivel {datos.get("Part 1-2")}, '
        f'se ha usado el arma {datos.get("Weapon Desc") or "Desconocida"} el dia {datos.get("DATE OCC")}, '
        f'a la hora {datos.get("TIME OCC")}, en {datos.get("AREA NAME")}, '
        f'distrito:{datos.get("Rpt Dist No")}, en un/a {datos.get("Premis Desc")}. '
        f'Informacion de la victima: edad={datos.get("Vict Age")}, sexo={datos.get("Vict Sex")}, '
        f'descendencia={datos.get("Vict Descent")}, '
        f'finalmente el caso será resuelto con {datos.get("Status Desc")}.'
    )

    classifier_instance = get_classifier()

    raw_estilo   = classifier_instance(texto, candidate_labels=c_estilo,   multi_label=True)
    raw_tematica = classifier_instance(texto, candidate_labels=c_tematica, multi_label=True)
    raw_fisicos  = classifier_instance(texto, candidate_labels=c_fisicos,  multi_label=True)
    raw_contexto = classifier_instance(texto, candidate_labels=c_contexto, multi_label=True)

    todas_etiquetas = {
        "labels_genericas":              _extraer_top(raw_estilo,   2),
        "labels_motivo_crimen":          _extraer_top(raw_tematica, 1),
        "labels_escena_caracteristicas": _extraer_top(raw_fisicos,  3),
        "labels_contexto_clasificacion": _extraer_top(raw_contexto, 2),
    }

    return {
        "etiqueta":         {cat: items[0]["label"] for cat, items in todas_etiquetas.items()},
        "confianza":        {cat: items[0]["score"] for cat, items in todas_etiquetas.items()},
        "texto_construido": texto,
        "todas_etiquetas":  todas_etiquetas,
        "modelo":           MODELO,
    }