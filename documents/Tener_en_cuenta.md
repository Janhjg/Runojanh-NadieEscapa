"""Con pydantic se crea un Base_Model del cual usara la api para rellenar los predict/new"""

Data set crudo -> panda -> ML -> huggin face -> IA generativa -> User

NOS CARGAMOS REGITROS CON MENOS DE DOS ANOS

### Categorias a Usar : 
- DR_NO -> ID único del crimen
- DATE OCC -> Fecha del crimen
- Time OCC -> Hora del crimen en formato 24h
- AREA NAME -> Nombre del barrio/división policial
- Crm Cd Desc-> Descripción del tipo de crimen
- Vict Age-> Edad de la víctima
- Vict Sex-> Sexo de la víctima (M/F/X/N)
- Premis Desc-> Lugar donde ocurrió (calle, apartamento, parking...)
- Weapon Desc-> Descripción del arma usada
- Status Desc-> Estado del caso (investigación, arrestado...)
- Part 1-2 -> Gravedad del crimen (1=grave, 2=leve)
- LOCATION -> Dirección redondeada al bloque



Plan historico




Crimen clasificado como {gravedad}: {datos['CRM_CD_DESC'].lower()} {crimen_secundario}
Ocurrio en {datos['AREA_NAME']}, Los Angeles, en {datos['LOCATION'].lower()}
por la {periodo} a las {hora_fmt}
Lugar del incidente: {datos['PREMIS_DESC'].lower()}
Victima de {datos['VICT_AGE']} años, sexo {datos['VICT_SEX']}, {arma}
Estado actual del caso: {datos['STATUS_DESC']}
El modelo predictivo estimacon {resolucion}