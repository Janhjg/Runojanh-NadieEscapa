# Idea inicial 

1: al abrir el frontend aparece una pantalla inicial con el nombre del proyecto/pagina y un boton de "empezar" o "iniciar" que lleva al usuario a la pantalla principal.
2: al tocar el boton iniciar se escucha una voz narrada de un texto X y empieza a sonar una musica de misterio de fondo durante el flujo de el frontend la cual tendra un boton o teclas asignadas para subir o bajar su volumen 
3: despues aparece un menu con las opciones de para ver los casos que estan ya en el dataset (los que en la api se procesan con el endpoint get /crimes y get /crimes/{id}) y otro boton solo para predecir con el modelo de ML los casos del dataset limpio (los que en la api se procesan con el endpoint  get /predict/{id}) y otro boton para clasificar los casos del dataset limpio (los que en la api se procesan con el endpoint get /classify y get /classify/{id}) y otro boton para generar la cronica de los casos del dataset limpio (los que en la api se procesan con el endpoint get /narrate y get /narrate/{id}) y otro boton para generar la cronica completa de los casos del dataset limpio (los que en la api se procesan con el endpoint get /full-case/new y get /full-case/{id}) y otro boton para ver los casos que estan ya en el dataset con su cronica completa (los que en la api se procesan con el endpoint get /full-case/new y get /full-case/{id})
Ademas todo para los nuevos casos creados por el usuario como tenemos actualmente
4 Cada boton te lleva a una nueva pestana con su propio diseno y estilo
5 Se puede navegar libremente en el frontlane entre las pestanas

