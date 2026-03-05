# Runojanh-NadieEscapa

# DEFINICION DEL PROYECTO
RunojAN es una API REST que transforma datos brutos de crímenes urbanos reales en narrativas de novela negra generadas por inteligencia artificial. El sistema integra tres capas tecnológicas — un modelo de Machine Learning predictivo, un clasificador de Hugging Face y un componente generativo basado en una IA generativa — para ofrecer una experiencia que va más allá del análisis estadístico convencional. Tambien es capaz de generar resultados a nuevos crimenes determinados por el usuario

## ¿Qué problema resuelve?
Los datasets de crímenes urbanos son vastos, fríos y técnicos. Contienen miles de registros con campos como tipo de delito, hora, barrio o estado del caso, pero su consulta directa requiere conocimientos de análisis de datos y no aporta ninguna dimensión humana ni narrativa. Este sistema resuelve tres problemas concretos:

Problema 1 — Acceso técnico: explorar un DATASET de millones de registros es inaccesible para usuarios no especializados.
Problema 2 — Falta de predicción: no existe una manera sencilla de estimar si un crimen sin resolver terminará en arresto.
Problema 3 — Ausencia de valor narrativo: los datos existen pero no comunican, no emocionan ni cuentan una historia.

# ¿Para quién está pensado?
El proyecto está dirigido a tres perfiles de usuario:

* Aficionados a la novela negra y al thriller criminal que quieran descubrir historias reales narradas con tensión literaria.
* Estudiantes y profesores de ciencia de datos que busquen un ejemplo práctico e integrado de ML + Modelo preentrenado + IA Generativa.

# ¿Qué valor aporta frente a simplemente analizar el dataset en un notebook?
La diferencia fundamental en nuestro sistema es técnica y experiencial. Un notebook muestra tablas, gráficas y métricas. Este sistema convierte esos mismos datos en una experiencia narrativa interactiva:

* Accesibilidad total: cualquier usuario consume los resultados vía API sin saber de Python ni de estadística.
* Clasificación dramática: Hugging Face etiqueta automáticamente cada crimen con una categoría narrativa que da contexto emocional.
* Narración generativa: La IA generativa convierte los datos técnicos en prosa literaria de género negro, transformando números en historia.

# ¿Por qué es necesario cada componente?
El caso de uso central es el siguiente: un usuario introduce los datos de un crimen — tipo, barrio, hora, día, uso de arma o ID de crimen del dataset — y el sistema responde con tres capas de valor que solo son posibles combinando los tres componentes:

Machine Learning (Trururu): sin este modelo no existe manera de estimar la probabilidad de resolución del caso. Es el componente predictivo que da utilidad práctica al sistema.
Hugging Face (Zero-Shot Classification): sin este modelo, el crimen llega a la IA Generativa como un dato técnico sin matiz dramático. La clasificación previa — crimen pasional, robo desesperado, venganza organizada, ect — es la que le indica a la IA Generativa el tono narrativo exacto que debe usar.
IA Generativa: sin este componente, el sistema solo devuelve porcentajes y etiquetas. la IA es quien transforma esos datos en una historia que el usuario quiera leer, cumpliendo el objetivo narrativo central del proyecto.

# DATASET ELEGIDO

## FUENTE DE DATOS
### LOS ANGELES CRIMEN DATA 2020-2023
 * #### https://www.kaggle.com/datasets/venkatsairo4899/los-angeles-crime-data-2020-2023?select=Crime_Data_from_2020_to_Present.csv

TIPO DE PROBLEMA: CLASIFICACION

Este dataset es adecuado para:
Modelo Machine Learning: Nos permite clasificar si un crimen lleva arresto o no en base a los registros del crimen.
Modelo Preentrenado: Podemos etiquetar el crimen en base a los datos que nos ofrece para darle un matiz narrativo.
IA Generativa: Nos da una idea mas visual, literaria e interesante del crimen dandole al usuario una experiencia narrativa , accesible y agradable.

# Tipo de aplicacion
* Servicio predictivo
* Servicio narrativo

# Ejemplo de uso real:

El usuario hace una peticion a trabes del endpoint POST/Narrate , le envia los datos del crimen o el ID de uno ya existente y el sistema le devuelve una narrativa de novela negra en  base a eeste caso.

Nuestro modelo nos dice si este crimen lleva un arresto o no, el modelo preentrenado etiqueta este crimen y la IA genera una narracion en base a esto.

# Arquitectura y encaje de piezas
## 2.1 Modelo propio de Machine Learning
* Clasificacion
* Status Desc
* Mediante endpoints

## 2.2 Modelo de Hugging Face
* Clasificacion
* Una etiqueta al crime
* Mediante Post y Gets

## 2.3 Modelo IA generativa
* Narrativa
* Mediante pronts

## 2.4 Exposicion
* Fast api
* ENDPOINTS:
- Consulta de Datos
GET/crimesLista crímenes del dataset con paginación
GET/crimes/{id}Obtiene un crimen específico por ID

- Modelo MachineLearning
POST/predict/arrestoPredice si el crimen será resuelto con arresto

- Huggin Face
POST/classify/dramatismoClasifica el crimen en categoría dramática
POST/classify/tonoDetermina el tono narrativo ideal
GET/classify/etiquetasLista todas las etiquetas dramáticas disponibles

- IA generativa
POST/narrate/crime Narra el crimen como una novela negra 

## IDEAS GENERALES 
1. En base a los arrestados en el dataset te diga que probabilidad hay de arresto a aquellos que aun estan siendo investigados, el modelo de ML te dice si llevan arresto o no
2. El modelo de HUggin Facce clasifica el crimen y le da un tono sentimental
3. La IA generativa genera una historia oscura en base al crimen

# FLUJO 
Dataset (crimen real)
      ↓
/predict   →  Random Forest  →  probabilidad de arresto: 23%
      ↓
/classify  →  HuggingFace  →  "robo desesperado" (61%)
      ↓
/narrate   →  Claude  →  capítulo de novela negra con ese tono
