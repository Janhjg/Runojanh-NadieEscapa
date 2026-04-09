from transformers import pipeline
import pandas as pd
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = ["Sórdido", "Inhóspito", "Decadente", "Opresivo", "Gélido", "Sombrío", "Derrotismo", "Apatía", "Alienación", "Desasosiego", "Tormento", "Escepticismo", "Trauma", "Lucidez amarga", "Perfidia", "Ensañamiento", "Resentimiento", "Ambigüedad moral", "Codicia", "Deslealtad", "Crueldad", "Incertidumbre", "Incomodidad", "Desconsuelo", "Vértigo", "Indignación", "Extrañeza"]
df=pd.read_csv("data\\crimeData_limpio.csv")

def construir_clasificacion(datos, VObjetiva):
    
    texto=f'Ocurrido el crimen {datos["Crm Cd Desc"]} de nivel {datos["Part 1-2"]}, se ha usado el arma {datos["Weapon Desc"]} el dia {datos["DATE OCC"]}, a la hora {datos["TIME OCC"]}, en {datos["AREA NAME"]}, distrito:{datos["Rpt Dist No"]}, en un/a {datos["Premis Desc"]}.'
    texto+=f'Informacion de la victima: edad= {datos["Vict Age"]}, sexo={datos["Vict Sex"]} descendencia={datos["Vict Descent"]}, finalmente el caso será resuelto con {VObjetiva}'
    result :dict= classifier(texto, candidate_labels=labels, multi_label=True)
    return result["labels"][:5]
