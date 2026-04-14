"""
test_narrative_consistency.py
Analiza el texto generado por Ollama e identifica inconsistencias
con los datos del crimen registrados.
"""
import sys
sys.path.insert(0, '.')

from services.generator_service import generar_cronica

# ─── CASOS DE PRUEBA ───────────────────────────────────────────────────────────
casos = [
    {
        "nombre": "Victima Femenina / Vehiculo / Homicidio",
        "datos": {
            "DATE OCC": "01/15/2024",
            "TIME OCC": 2300,
            "AREA NAME": "Hollywood",
            "Rpt Dist No": 605,
            "Part 1-2": 1,
            "Crm Cd Desc": "HOMICIDE",
            "Vict Age": 10,
            "Vict Sex": "F",
            "Vict Descent": "H",
            "Premis Desc": "STREET",
            "Weapon Desc": "VEHICLE",
            "Status Desc": "Investigating"
        },
        "prediccion": {"clase_predicha": "arrestado", "confianza": 0.58},
        "etiquetas": {"labels_genericas": [{"label": "triste"}, {"label": "calculado"}],
                      "labels_motivo_crimen": [{"label": "homicidio"}],
                      "labels_escena_caracteristicas": [{"label": "cuerpo abandonado"}, {"label": "ocultamiento"}],
                      "labels_contexto_clasificacion": [{"label": "víctima menor"}, {"label": "conocido"}]},
        "verificaciones": {
            "debe_contener": ["ella", "niña", "su cuerpo"],
            "no_debe_contener": ["él disparó", "pólvora", "casquillo", "el hombre yacía"],
            "arma": "VEHICLE",
            "sexo": "F"
        }
    },
    {
        "nombre": "Victima Masculina / Arma de fuego / Robo",
        "datos": {
            "DATE OCC": "03/10/2024",
            "TIME OCC": 130,
            "AREA NAME": "Newton",
            "Rpt Dist No": 2100,
            "Part 1-2": 1,
            "Crm Cd Desc": "ROBBERY",
            "Vict Age": 45,
            "Vict Sex": "M",
            "Vict Descent": "B",
            "Premis Desc": "SIDEWALK",
            "Weapon Desc": "HAND GUN",
            "Status Desc": "Adult Arrest"
        },
        "prediccion": {"clase_predicha": "arrestado", "confianza": 0.72},
        "etiquetas": {"labels_genericas": [{"label": "frío"}, {"label": "calculado"}],
                      "labels_motivo_crimen": [{"label": "robo con violencia"}],
                      "labels_escena_caracteristicas": [{"label": "arma de fuego"}, {"label": "huellas"}],
                      "labels_contexto_clasificacion": [{"label": "callejero"}, {"label": "violento"}]},
        "verificaciones": {
            "debe_contener": [],
            "no_debe_contener": ["ella", "niña"],
            "arma": "HAND GUN",
            "sexo": "M"
        }
    }
]

# ─── ANALIZADOR DE CONSISTENCIA ────────────────────────────────────────────────
def analizar_texto(cronica: str, verificaciones: dict, nombre_caso: str):
    texto_lower = cronica.lower()
    errores = []
    advertencias = []

    # Verificar palabras obligatorias
    for palabra in verificaciones["debe_contener"]:
        if palabra.lower() not in texto_lower:
            advertencias.append(f"  ⚠️  Se esperaba '{palabra}' pero no aparece")

    # Verificar palabras prohibidas
    for palabra in verificaciones["no_debe_contener"]:
        if palabra.lower() in texto_lower:
            errores.append(f"  ❌ Inconsistencia: aparece '{palabra}' pero NO debería")

    # Verificar coherencia de género
    sexo = verificaciones["sexo"]
    if sexo == "F":
        if " él " in texto_lower or "el hombre" in texto_lower or "del hombre" in texto_lower:
            errores.append("  ❌ GÉNERO INCORRECTO: se usa pronombre masculino para víctima femenina")
        if "ella" in texto_lower or "niña" in texto_lower or "mujer" in texto_lower:
            pass  # OK
        else:
            advertencias.append("  ⚠️  No se detectan pronombres femeninos ('ella', 'mujer', 'niña')")
    elif sexo == "M":
        if "ella " in texto_lower:
            errores.append("  ❌ GÉNERO INCORRECTO: se usa pronombre femenino para víctima masculina")

    # Verificar coherencia del arma
    arma = verificaciones["arma"].upper()
    firearms = ["GUN", "PISTOL", "REVOLVER", "RIFLE", "FIREARM"]
    is_firearm = any(k in arma for k in firearms)
    
    if not is_firearm:
        if "disparo" in texto_lower or "pólvora" in texto_lower or "casquillo" in texto_lower or "bala" in texto_lower:
            errores.append(f"  ❌ ARMA INCORRECTA: se mencionan balas/disparos pero el arma es '{arma}'")

    return errores, advertencias


# ─── EJECUTAR PRUEBAS ──────────────────────────────────────────────────────────
for caso in casos:
    print(f"\n{'='*65}")
    print(f"  CASO: {caso['nombre']}")
    print(f"{'='*65}")
    print(f"  Generando crónica con Ollama...")
    
    cronica = generar_cronica(caso["datos"], caso["prediccion"], caso["etiquetas"])
    
    print(f"\n  --- CRÓNICA GENERADA ---")
    print(cronica)
    
    print(f"\n  --- ANÁLISIS DE CONSISTENCIA ---")
    errores, advertencias = analizar_texto(cronica, caso["verificaciones"], caso["nombre"])
    
    if not errores and not advertencias:
        print("  ✅ Sin inconsistencias detectadas")
    for e in errores:
        print(e)
    for a in advertencias:
        print(a)
    
    print(f"\n  RESULTADO: {'❌ FALLO' if errores else '✅ OK'} ({len(errores)} errores, {len(advertencias)} advertencias)")
