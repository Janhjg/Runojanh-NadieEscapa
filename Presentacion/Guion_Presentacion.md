# GUION DE PRESENTACIÓN: "EL VEREDICTO DE CRISTAL"

## 1. El Despertar de la Máquina

**AUDIO PREGRABADO:** [Reproduce el audio introductorio / El Gancho Noir]
- *Después del "3, 2, 1" del audio:* **(SE COMPARTE PANTALLA COMPLETA CON EL PROGRAMA EN LA PANTALLA PRINCIPAL)**

**PERSONA 1:** "Bienvenidos a Runojanh. Nadie escapa a partir de ahora."

**PERSONA 1:** "Estamos ante la puerta de Los Ángeles. Más de 660,000 secretos esperando ser desenterrados." 

**PERSONA 2:** "El sistema está corriendo sobre Next.js para una respuesta inmediata. ¿Iniciamos?" 

**PERSONA 3:** "Hazlo. Despierta a la máquina."

*(Persona 2 hace clic en el botón INICIAR en la pantalla.* 
*- Suena la música de misterio y la voz de la IA dando la bienvenida).*

**PERSONA 1:** "La música de fondo ya está sincronizada. Es el latido de la ciudad. ¿Resulta abrumador a sus oídos? Podemos bajarla para ustedes." *(Muestra cómo ajustar el volumen)*

---

## 2. Monitor Táctico y Archivos (Introducción a los Datos)

*(Persona 2 navega al **Monitor Táctico** y a la tabla de crímenes)*

**PERSONA 1:** "Miren esto. No son solo filas en una tabla. Son crímenes reales de L.A. Cada punto que filtramos es una tragedia que el sistema ha procesado desde nuestra base de datos central."

**PERSONA 2:** "La API nos devuelve estos miles de casos en milisegundos. Podemos buscar por arma, por zona... el sistema no descansa." 

**PERSONA 3:** "Observen la precisión. El backend limpia y organiza el caos para que nosotros solo tengamos que investigar. Además, contamos con nuestro **Monitor Táctico**, un mapa en tiempo real donde la ciudad se pinta con las probabilidades y focos de criminalidad basándose en los filtros aplicados."

**PERSONA 1:** "Pero la ciudad no es estática. Las calles siguen sangrando. Por eso hemos implementado la capacidad de **crear un nuevo caso**. Podemos ingresar manualmente un crimen en progreso o los detalles de una nueva escena, y Runojanh lo procesará con el mismo rigor que los 660,000 casos históricos."

---

## 3. Inteligencia Artificial: Predicción y Clasificación

*(Navegan a las secciones de Análisis / Predecir / Clasificar)*

**PERSONA 1:** "Vamos a ver qué piensa la inteligencia artificial de este caso en particular."

**PERSONA 3:** "Estamos usando modelos de Zero-Shot y Machine Learning."
> **[Explicación en vivo - ML y Zero-Shot]:**  
> *"Hemos entrenado un modelo de Machine Learning propio (Random Forest) utilizando las variables geográficas y temporales de nuestro inmenso dataset para que identifique patrones y prediga la probabilidad de arresto. Por otro lado, para el Zero-Shot, usamos BART-Large de Hugging Face. Es un modelo pre-entrenado deductivo al que no le damos casos resueltos, sino que con el simple contexto del crimen etiqueta las temáticas policiales que lo caracterizan."*

**PERSONA 3 (Continúa):** "No le hemos dicho a la máquina qué buscar; ella misma deduce el tipo de crimen y calcula las probabilidades de que el sospechoso logre escapar."

**PERSONA 2:** "Es análisis puro. Sin errores humanos. La lógica de Ollama y nuestros modelos predictivos trabajando en paralelo."
> **[Explicación en vivo - Prompt de Ollama]:**  
> *"En el caso de Ollama, usamos técnicas de Prompt Engineering. Le inyectamos los datos fríos del lugar, la hora y el arma, junto con los resultados de las predicciones. Todo eso bajo una instrucción clara para que el modelo redacte el suceso no como una IA, sino en tono de novela negra, como si fuera un detective relatando la tragedia."*

---

## 4. Arquitectura Transparente (La API)

*(Persona 2 abre una nueva pestaña mostrando la documentación de la API / Swagger en `localhost:8001/docs` o simplemente el código fuente del backend)*

**PERSONA 1:** "Pero Runojanh no es solo una interfaz bonita. Lo que ven en pantalla está alimentado por una arquitectura robusta."

**PERSONA 2:** "El frontend y el backend están completamente desacoplados. Hemos construido una API RESTful con FastAPI en Python que orquesta todo el flujo. Tenemos endpoints dedicados para consultar el dataset, realizar predicciones rápidas, clasificar textos e interactuar con Ollama."

**PERSONA 3:** "Esta modularidad significa que cualquier agencia de seguridad, o cualquier otra aplicación, podría conectarse a nuestra API y utilizar nuestros modelos entrenados sin necesidad de usar nuestra interfaz. Es un motor de inteligencia criminal escalable y abierto."

---

## 5. El Veredicto: Evidencia en PDF y Casos Nuevos

*(Vuelven a la interfaz táctica y abren uno de los **Casos Nuevos** creados o la sección de Full Case)*

**PERSONA 1:** "Una vez que el sistema ha procesado la información, ya sea de un caso histórico o de un **nuevo caso** que hayamos introducido manualmente, la investigación concluye."
> **[Leer una parte de la narrativa escrita por la IA en pantalla]**  
> *(Ejm: "Eran las 3 de la mañana en las oscuras calles de Central...")*

**PERSONA 2:** "Todo queda empaquetado y listo para descargar... Y ahora obtendremos todo el expediente." 
*(Hace clic para generar y descargar el **PDF** del caso, mostrando cómo también funciona para los nuevos expedientes).* 
**PERSONA 2 (Continúa):** "Desde el código hasta el documento final, el flujo ha sido perfecto. Generados al instante."

**PERSONA 3:** "Porque en Runojanh, los datos nunca mueren... solo esperan a ser encontrados."

**PERSONA 1:** "Y como siempre decimos aquí: Nadie Escapa."
