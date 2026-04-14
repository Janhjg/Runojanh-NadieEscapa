import os
import sys
from traductor_crimenes_service import traductor_datosCrimen
from ollama import chat
from ollama import ChatResponse



def generar_historia(data, etiquetas_dict, Vobjetiva=None) -> str:
    # tipo de ETIQUETAS y cuantas contiene
    # labels_genericas, 2
    # labels_motivo_crimen, 1
    # labels_escena_caracteristicas, 3
    # labels_contexto_clasificacion, 2
    # ejemplo ["nombre etiqueta"][0] o [:2](para que devuelva las dos)

    if Vobjetiva:
      # para casos nuevos
      data=traductor_datosCrimen(data, Vobjetiva)
    else: data=traductor_datosCrimen(data)
    
    prompt=""
    
    # gemma4:e2b
    response: ChatResponse = chat(model='', messages=[
    {
      'role': 'user',
      'content': prompt,
    },
  ])

    return response.message.content

if __name__ == "__main__":
    print(generar_historia(None))
#     df=pd.read_csv("data\\crimeData_limpio.csv")
# if __name__=="__main__":
#    print(construir_clasificacion(df.iloc[6220],df.iloc[6220]["Status Desc"]))
    # texto = input("Tú: ")
    # resultado = preguntar_a_grok(texto)
    # print(f"Grok: {resultado}")