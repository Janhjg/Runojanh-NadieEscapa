# 🕵️‍♂️ Runojanh - Nadie Escapa: Terminal de Inteligencia Criminal

## 🌑 Definición del Proyecto
**Runojanh** es una plataforma de análisis criminal inmersiva que transforma la frialdad de los datos estadísticos de Los Ángeles (2020-2023) en una experiencia narrativa de género **Noir**. Mediante la integración de modelos de **entrenamiento propio**, clasificadores de lenguaje natural y motores generativos de última generación, el sistema no solo analiza crímenes, sino que los narra, permitiendo a los investigadores (usuarios) explorar la dimensión humana y dramática oculta tras cada expediente.

---

## 🛠️ Tridente Tecnológico (El Núcleo)

Nuestro sistema se apoya en tres pilares fundamentales de Inteligencia Artificial que trabajan en sincronía:

### 1. 🧠 ML Propio: El Oráculo Entrenado (Random Forest)
A diferencia de usar APIs externas, **hemos diseñado y entrenado nuestro propio modelo de Machine Learning** utilizando una arquitectura de **Random Forest**.
- **Entrenamiento:** Entrenado con más de 660,000 expedientes reales de la LAPD tras un proceso exhaustivo de limpieza y selección de características (feature engineering).
- **Función:** Clasificación binaria (Arresto: Sí/No).
- **Valor Técnico:** Un modelo optimizado por nosotros para detectar patrones específicos de criminalidad urbana, ofreciendo una predicción de éxito operativa.

### 2. 🏷️ NLP: Clasificador de Matices (BART-Large)
Implementamos el modelo **BART-Large-MNLI** de Hugging Face para realizar clasificación *zero-shot*.
- **Función:** Etiquetado dramático y psicológico del caso.
- **Valor:** Proporciona el ADN emocional del caso, dictando el tono que la narrativa debe seguir.

### 3. ✍️ IA Generativa: El Cronista de la Ciudad (Gemini 2.0 / Llama)
El motor final toma los datos técnicos, la predicción de **nuestro modelo** y las etiquetas dramáticas para generar una narrativa literaria Noir de alta fidelidad.

---

## 🏗️ Arquitectura del Sistema

| Módulo | Tecnología | Rol en la Investigación |
| :--- | :--- | :--- |
| **ML Engine** | **Random Forest (Entrenamiento Propio)** | Predicción científica de resolución de casos. |
| **Frontend** | Next.js + Tailwind + Framer Motion | Interfaz de terminal Noir inmersiva con audio dinámico. |
| **Backend** | FastAPI (Python) | Orquestación de modelos y exposición de la API REST. |
| **Modelos NLP** | BART + Gemini/Ollama | Inteligencia clasificatoria y narrativa. |

---

**"En esta ciudad, los datos no mienten, pero solo la IA sabe contar sus historias."**
