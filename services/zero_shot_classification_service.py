from transformers import pipeline
import pandas as pd
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels_genéricas_basicas = ["sangriento", "gore", "frío", "calculado", "impulsivo", "triste", "sin sentido", "sádico", "enfermizo", "pasional", "vengativo", "accidental", "misterioso", "ritual", "serial", "masacre", "ejecución", "narco", "cartel", "psicópata", "organizado", "desorganizado", "caótico", "limpio", "sucio", "sobre-ensañamiento"]
labels_tipo_motivo_crimen = ["homicidio", "homicidio múltiple", "familiar", "secuestro", "tortura", "asfixia", "apuñalamiento", "disparo", "estrangulamiento", "golpeamiento", "envenenamiento", "ahogamiento", "incendio", "robo con violencia", "agresión sexual", "doméstico", "pasional", "celos", "discusión", "drogas", "venganza", "accidente", "suicidio disfrazado", "ejecución profesional"]
labels_escena_características = ["escena caótica", "escena limpia", "alta limpieza", "ocultamiento", "fosa", "maletero", "cuerpo abandonado", "sangre en paredes", "huellas ensangrentadas", "trofeos", "grabaciones", "tortura psicológica", "tiro de gracia", "manos atadas", "vendados", "bolsa en cabeza", "cuchillo", "arma de fuego", "arma blanca", "arma improvisada"]
labels_contexto_clasificación = ["violento", "propiedad", "callejero", "barrio", "rural", "urbano", "organizado crime", "narcotráfico", "intrafamiliar", "extraño", "conocido", "víctima menor", "víctima vulnerable", "tragedia evitable", "por nada", "estupidez fatal", "sin alma", "frío como el hielo", "disfrute del sufrimiento", "coleccionista"]
df=pd.read_csv("data\\crimeData_limpio.csv")

def traductor_datosCrimen(datos :dict, VObjetiva):
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
    if VObjetiva=="Adult Arrest" or VObjetiva=="Juv Arrest":
        datos["Status Desc"]="Arresto"
    elif VObjetiva=="Adult Other" or VObjetiva=="Juv Other":
        datos["Status Desc"]="No arresto"
    else:
        datos["Status Desc"]="Caso en Investigacion"
    


    return datos
def construir_clasificacion(datos, VObjetiva):
    datos=traductor_datosCrimen(datos, VObjetiva)
    texto=f'Ocurrido el crimen {datos["Crm Cd Desc"]} de nivel {datos["Part 1-2"]}, se ha usado el arma {datos["Weapon Desc"]} el dia {datos["DATE OCC"]}, a la hora {datos["TIME OCC"]}, en {datos["AREA NAME"]}, distrito:{datos["Rpt Dist No"]}, en un/a {datos["Premis Desc"]}.'
    texto+=f'Informacion de la victima: edad= {datos["Vict Age"]}, sexo={datos["Vict Sex"]} descendencia={datos["Vict Descent"]}, finalmente el caso será resuelto con {datos["Status Desc"]}'
    resultadoLabel_genericas_basicas  :list= classifier(texto, candidate_labels=labels_genéricas_basicas , multi_label=True)["labels"]
    resultadoLabel_tipo_motivo_crimen :list= classifier(texto, candidate_labels=labels_tipo_motivo_crimen, multi_label=True)["labels"]
    resultadoLabel_escena_caracteristicas :list= classifier(texto, candidate_labels=labels_escena_características, multi_label=True)["labels"]
    resultadoLabel_contexto_clasificacion :list= classifier(texto, candidate_labels=labels_contexto_clasificación, multi_label=True)["labels"]
    resultado_final_labels_totales={
        "labels_genericas":resultadoLabel_genericas_basicas[:2],
        "labels_motivo_crimen":resultadoLabel_tipo_motivo_crimen[:1],
        "labels_escena_caracteristicas":resultadoLabel_escena_caracteristicas[:3],
        "labels_contexto_clasificacion":resultadoLabel_contexto_clasificacion[:2]
    }
    return resultado_final_labels_totales

print(construir_clasificacion(df.iloc[350],df.iloc[350]["Status Desc"]))


# Etiquetas genéricas básicas: sangriento, gore, frío, calculado, impulsivo, triste, sin sentido, sádico, enfermizo, pasional, vengativo, accidental, misterioso, ritual, serial, masacre, ejecución, narco, cartel, psicópata, organizado, desorganizado, caótico, limpio, sucio, sobre-ensañamiento

# Etiquetas de tipo/motivo del crimen: homicidio, homicidio múltiple, familiar, secuestro, tortura, asfixia, apuñalamiento, disparo, estrangulamiento, golpeamiento, envenenamiento, ahogamiento, incendio, robo con violencia, agresión sexual, doméstico, pasional, celos, discusión, drogas, venganza, accidente, suicidio disfrazado, ejecución profesional

# Etiquetas de escena / características forenses: escena caótica, escena limpia, alta limpieza, ocultamiento, fosa, maletero, cuerpo abandonado, sangre en paredes, huellas ensangrentadas, trofeos, grabaciones, tortura psicológica, tiro de gracia, manos atadas, vendados, bolsa en cabeza, cuchillo, arma de fuego, arma blanca, arma improvisada

# Etiquetas de contexto / clasificación general: violento, propiedad, callejero, barrio, rural, urbano, organizado crime, narcotráfico, intrafamiliar, extraño, conocido, víctima menor, víctima vulnerable, tragedia evitable, por nada, estupidez fatal, sin alma, frío como el hielo, disfrute del sufrimiento, coleccionista
if __name__=="__main__":
   print(construir_clasificacion(df.iloc[6220],df.iloc[6220]["Status Desc"]))