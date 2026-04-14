def traductor_datosCrimen(datos: dict, VObjetiva=None):

    # NIVEL
    datos["Part 1-2"] = "Muy Importante" if datos["Part 1-2"] == 1 else "Poco Importante"

    # SEXO
    sexo_map = {"F": "Femenino", "M": "Masculino"}
    datos["Vict Sex"] = sexo_map.get(datos.get("Vict Sex"), "Desconocido")

    # DESCENDENCIA — ✅ .get() para no explotar con valores raros
    diccionarioDescendencia = {
        "A": "Asiática", "B": "Negra", "C": "China", "D": "Camboyana",
        "F": "Filipina", "G": "Guameña", "H": "Hispana/Latinoamericana",
        "I": "Indígena americana", "J": "Japonesa", "K": "Coreana",
        "O": "Otros", "P": "Isleña del Pacífico", "S": "Samoana",
        "U": "Hawaiana", "V": "Vietnamita", "W": "Blanca",
        "X": "Desconocida", "Z": "Asiático indio"
    }
    datos["Vict Descent"] = diccionarioDescendencia.get(datos.get("Vict Descent"), "Desconocida")

    # ESTADO DEL CASO — ✅ ahora traduce aunque VObjetiva sea None
    if VObjetiva in ("Adult Arrest", "Juv Arrest", "arrestado"):
        datos["Status Desc"] = "Arresto"
    elif VObjetiva in ("Adult Other", "Juv Other", "no arrestado"):
        datos["Status Desc"] = "No arresto"
    else:
        datos["Status Desc"] = "Caso en Investigacion"

    return datos