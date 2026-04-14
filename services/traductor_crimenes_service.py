def traductor_datosCrimen(datos :dict, VObjetiva=None):
    #Traducciendo variables para hacer el texto mas legible.
    
    #NIVEL
    if datos["Part 1-2"]==1:
        datos["Part 1-2"]="Muy Importante"
    else:
        datos["Part 1-2"]="Poco Importante"

    #SEXO
    if datos["Vict Sex"]=="F":
        datos["Vict Sex"]="Femenino"
    elif datos["Vict Sex"]=="M":
        datos["Vict Sex"]="Masculino"
    else:
        datos["Vict Sex"]="Desconocido"

    #DESCENDENCIA
    diccionarioDescendencia={
        "A": "Asiática",
        "B": "negra",
        "C": "China",
        "D": "Camboyana",
        "F": "Filipina",
        "G": "Guameña",
        "H": "Hispana / latinoamericana / mexicana",
        "I": "Indígena americana / nativas de Alaska",
        "J": "japonesa",
        "K": "Coreana",
        "O": "Otros",
        "P": "De isla del Pacífico",
        "S": "Samoana",
        "U": "Hawaiano",
        "V": "Vietnamita",
        "W": "Persona blanca",
        "X": "Desconocida",
        "Z": "Asiático indio"
    }
    datos["Vict Descent"]=diccionarioDescendencia[datos["Vict Descent"]]

    #Estado del caso
    if VObjetiva:
        if VObjetiva=="Adult Arrest" or VObjetiva=="Juv Arrest":
            datos["Status Desc"]="Arresto"
        elif VObjetiva=="Adult Other" or VObjetiva=="Juv Other":
            datos["Status Desc"]="No arresto"
        else:
            datos["Status Desc"]="Caso en Investigacion"
    
    return datos