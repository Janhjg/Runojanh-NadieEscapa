# ROL: DATA
Responsable de todo lo relacionado con datos, modelos y análisis
Setup & Infraestructura. Definir estructura de carpetas del proyecto
Configurar .env con variables de entorno

1. Dataset

- Investigar y seleccionar el dataset final
- Descargar el dataset
- Exploración inicial del dataset
- Limpieza de datos
- Filtrar columnas relevantes
- Crear script de carga del dataset
- Documentar columnas usadas
- Crear subset de datos para pruebas

2. Modelo ML

- Definir la variable objetivo
- Seleccionar features del dataset
- Entrenar modelo
- Evaluar métricas del modelo
- Guardar modelo
- Guardar encoders
- Crear script train.py
- Documentar resultados del modelo

3. HuggingFace

- Investigar y confirmar modelo
- Definir las etiquetas narrativas finales
- Implementar construir_contexto(datos, prediccion)
- Integrar pipeline zero-shot classification
- Probar clasificación con casos reales
- Documentar etiquetas y criterios

4. IA Generativa

- Diseñar el prompt narrativo
- Ajustar el prompt según la etiqueta HuggingFace
- Probar narraciones con los tipos de crimen
- Validar longitud y calidad del texto
- Validar que el texto no expone datos técnicos
- Documentar el prompt final

5. Documentación

- Redactar sección 1.4 Descripción del dataset
- Redactar sección 1.5 Descripción del modelo ML
- Redactar sección 1.6 Descripción del modelo HuggingFace
- Redactar sección 1.7 Descripción del componente generativo

# ROL: DEV
Responsable de la API, integración de modelos y arquitectura del sistema

1. Setup & Infraestructura

- Crear repositorio en GitHub
- Crear entorno virtual Python
- Crear requirements.txt con todas las dependencias
- Configurar .gitignore
- Crear README.md inicial
- Configurar ramas main y dev

2. IA Generativa

- Implementar módulo narrator.py
- Conectar con la API de Anthropic

3. API FastAPI

- Crear estructura base de la API
- Implementar GET /crimes
- Implementar GET /crimes/{id}
- Implementar POST /predict/new
- Implementar GET /predict/{id}
- Implementar POST /classify
- Implementar POST /narrate
- Implementar POST /full-case/new
- Implementar GET /full-case/{id}
- Definir schemas Pydantic
- Configurar manejo de errores HTTP
- Verificar documentación Swagger

3. Documentación
- 
- Redactar sección 1.2 Arquitectura del sistema
- Redactar sección 1.3 Descripción de endpoints
- Actualizar README.md final

4. Entrega

- Revisión final del código
- Subir versión final a GitHub

# ROL: QA
Responsable de tests, calidad y documentación de entrega

1. Setup & Infraestructura

- (Soporte en revisión de estructura definida por DEV)

2. Tests

- Configurar entorno de testing con pytest
- Test 1 — GET /crimes casos válidos
- Test 1 — GET /crimes casos de error
- Test 2 — GET /crimes/{id} casos válidos
- Test 2 — GET /crimes/{id} casos de error
- Test 3 — POST /predict/new casos válidos
- Test 3 — POST /predict/new casos de error
- Test 4 — GET /predict/{id} casos válidos
- Test 4 — GET /predict/{id} casos de error
- Test 5 — POST /classify casos válidos
- Test 5 — POST /classify casos de error
- Test 6 — POST /narrate casos válidos
- Test 6 — POST /narrate casos de error
- Test 7 — POST /full-case/new integración
- Test 8 — GET /full-case/{id} integración
- Ejecutar todos los tests
- Documentar cobertura de tests

3. Documentación

- Redactar sección 1.1 Propósito del sistema
- Documentar los tests definidos

4. Entrega

- Revisión final de la documentación
- Grabación de demo del proyecto
- Preparar presentación del proyecto