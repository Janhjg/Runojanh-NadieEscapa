from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = [""]
def construir_contexto(datos, prediccion):
    
    texto=f"Ocurrido el crimen {datos["Crm Cd Desc"]} de nivel {datos["Part 1-2"]}, se ha usado el arma {datos["Weapon Used Desc"]} el dia {datos["DATE OCC"]}, a la hora {datos["TIME OCC"]}, en {datos["AREA NAME"]}, distrito:{datos["Rpt Dist No"]},{datos["LOCATION"]}, en un/a {datos["Premis Desc"]}.\n"
    texto+=f"Informacion de la victima: edad= {datos["Vict Age"]}, sexo={datos["Vict Sex"]} descendencia={datos["Vict Descent"]}, finalmente el caso será resuelto con {prediccion}"
    result :dict= classifier(texto, candidate_labels=labels, multi_label=True)
    return result["labels"][:5]