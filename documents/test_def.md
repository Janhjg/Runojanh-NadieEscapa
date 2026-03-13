# Test Api

## Test 1 : Get/crime 
* Devuelve los crimenes del dataset y seleccionas la cantidad de ellos.
- Verifica que devuelve la cantidad correcta.
- Verifica que Limit no sea mayor que la cantidad total de registros
- Verifica que salte una Http/Exception si el numero es negativo
- Si el valor es nulo o != numero lanza un Http/Exception
- Verificar que devuelva las columnas correctas
- Verificar que el offset funcione correctamente, al pedir los registros del 10 al 20 que devuelva exactamente esos.
- Si limit es 0 devuelve Http/Exception
- Verificar que la cantidad de casos devueltos sea igual a la cantidad pedida en el limit
- Verifica que se devuelva el/los crimen en la fecha o margen de fecha indicada
- Verifica que los crimenes devueoltos en fecha o margen de fecha son correctos

## Test 2 : Get/crime/ID
* Selecciona un crimen especifico en base a su ID
- Verifica que el ID exista sino lanza una Httpp/exception
- Verifica que el crimen tenga los valores y columnas requeridos correctos

# Test 3: Post/Predict/New
* Descripción: *Predice si un caso nuevo enviado manualmente resultará en arresto.

- Con todos los campos correctos devuelve True o False
- Que la respuesta coincide con la clase de mayor probabilidad

Falta algún campo obligatorio → HTTP 422
district con valor no existente → HTTP 422
hour fuera del rango 0-23 → HTTP 422
month fuera del rango 1-12 → HTTP 422
day_of_week fuera del rango 0-6 → HTTP 422
Body vacío → HTTP 422
Tipos de datos incorrectos (string donde va int) → HTTP 422

# Test 4: Get/Predict/ID
* ID existente con caso en investigación devuelve clase_predicha correctamente
* Clase_predicha es exactamente "arrestado" o "no arrestado"
* Clase_predicha coincide con la probabilidad más alta
* Los datos del caso recuperado coinciden con el dataset original
* ID inexistente → HTTP 404
* ID negativo → HTTP 422
* ID no numérico "abc" → HTTP 422
* ID = 0 → HTTP 422
* ID de caso que ya tiene Arrest = True en el dataset → HTTP 400 con mensaje "Este caso ya fue resuelto, no requiere predicción"
* ID de caso que ya tiene Arrest = False confirmado (cerrado sin arresto) → HTTP 400 con mensaje "Este caso ya fue cerrado sin arresto"

# Test 5: Post/Classify
* Descripción: Recibe los datos del crimen junto con la predicción del modelo ML, construye el texto narrativo y devuelve una etiqueta sentimental generada

- Con todos los campos correctos devuelve una etiqueta que pertenece exactamente a las etiquetas definidas
- La etiqueta ganadora tiene el score más alto de todas
- El campo texto_construido devuelve el texto que se le pasó a HuggingFace
- La etiqueta cambia si cambia la clase_predicha del ML manteniendo el resto de datos igual
- Dos crimenes del mismo tipo pero en distritos distintos pueden devolver etiquetas distintas

- Body vacío → HTTP 422
- Falta cualquier campo del crimen → HTTP 422
- Falta la prediccion_ml → HTTP 422
- clase_predicha con valor distinto a "arrestado" o "no arrestado" → HTTP 422
- Fallo del modelo HuggingFace → HTTP 503 con mensaje "Servicio de clasificación no disponible"

# Test 6: Post/Narrate
* Descripción: Recibe los datos del crimen, la predicción del modelo ML y la etiqueta de HuggingFace, y genera una crónica de novela negra usando IA Generativa.

* Devuelve un texto que no este vacío
* El texto tiene más de 100 palabras
* El texto menciona el barrio del crimen
* El texto menciona el tipo de crimen
* Dos llamadas con los mismos datos devuelven textos diferentes
* El texto no contiene los campos técnicos crudos del JSON como "probabilidad_arrestado": 0.18

* Body vacío → HTTP 422
* Falta datos_crimen → HTTP 422
* Falta prediccion_ml → HTTP 422
* Falta etiqueta_huggingface → HTTP 422
* etiqueta_huggingface con valor no perteneciente a las etiquetas definidas → HTTP 422
* clase_predicha con valor distinto a "arrestado" o "no arrestado" → HTTP 422
* Fallo de la API generativa  → HTTP 503 con mensaje "Servicio de narración no disponible"
* Timeout de la API de Anthropic superando 30 segundos → HTTP 504



### Cosas para recordar : 
Validar con excepciones personalizadas (katapasswordvalidator)
test client test fast api 
https://github.com/Janhjg/Kata/tree/aaaaaa/password_validator 