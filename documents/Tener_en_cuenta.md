"""Con pydantic se crea un Base_Model del cual usara la api para rellenar los predict/new"""

Data set crudo -> panda -> ML -> huggin face -> IA generativa -> User

NOS CARGAMOS REGITROS CON MENOS DE DOS ANOS

### Categorias a usar para entrenamiento: 
- ``DATE OCC``(str) **->**  Fecha del crimen
- ``TIME OCC``(int64) **->** Hora del crimen en formato 24h
- ``AREA``(int64) **->** referencia codificada de ``AREA NAME`` nombre del barrio/división policial
- ``Rpt Dist No``(int64) **->** Nº sector de barrio.
- ``Part 1-2``(int64) **->** Gravedad del crimen (1=grave, 2=leve)
- ``Crm Cd``(int64) **->** referencia codificada de ``Crm Cd Desc`` Descripción del tipo de crimen
- ``Vict Age``(int64) **->** Edad de la víctima
- ``Vict Sex``(str) **->**  Sexo de la víctima (M/F/X)
- ``Vict Descent``(str) **->** Descendencia de la víctima
- ``Premis Cd``(int64) **->** Referencia codificada de ``AREA NAME`` Lugar donde ocurrió (calle, apartamento, parking...)
- ``Weapon Used``Cd(int64) **->** Referencia codificada de ``Weapon Desc`` Descripción del arma usada
- ``Status Desc``(str) **->**  Variable objetivo representa el estado del caso (investigación, arrestado...)
- ``Crm Cd 2``(int64) **->** Codificacion de crimen adicional
- ``Crm Cd 3``(int64) **->** Codificacion de crimen adicional
- ``Crm Cd 4``(int64) **->** Codificacion de crimen adicional

### Categorias a usar para input, prediccion de caso nuevo: 
- ``DATE OCC``(str) **->**  Fecha del crimen
- ``TIME OCC``(int64) **->** Hora del crimen en formato 24h
- ``AREA NAME``(int64) **->** referencia codificada de ``AREA NAME`` nombre del barrio/división policial
- ``Rpt Dist No``(int64) **->** Nº sector de barrio.
- ``Part 1-2``(int64) **->** Gravedad del crimen (1=grave, 2=leve)
- ``Crm Cd Desc``(int64) **->** referencia codificada de ``Crm Cd Desc`` Descripción del tipo de crimen
- ``Vict Age``(int64) **->** Edad de la víctima
- ``Vict Sex``(str) **->**  Sexo de la víctima (M/F/X)
- ``Vict Descent``(str) **->** Descendencia de la víctima
- ``Premis Desc``(int64) **->** Referencia codificada de ``AREA NAME`` Lugar donde ocurrió (calle, apartamento, parking...)
- ``Weapon Desc``Cd(int64) **->** Referencia codificada de ``Weapon Desc`` Descripción del arma usada
- ``Status Desc``(str) **->**  Variable objetivo representa el estado del caso (investigación, arrestado...)
- ``Crm Cd 2``(int64) **->** Codificacion de crimen adicional
- ``Crm Cd 3``(int64) **->** Codificacion de crimen adicional
- ``Crm Cd 4``(int64) **->** Codificacion de crimen adicional

Plan historico




Crimen clasificado como {gravedad}: {datos['CRM_CD_DESC'].lower()} {crimen_secundario}
Ocurrio en {datos['AREA_NAME']}, Los Angeles, en {datos['LOCATION'].lower()}
por la {periodo} a las {hora_fmt}
Lugar del incidente: {datos['PREMIS_DESC'].lower()}
Victima de {datos['VICT_AGE']} años, sexo {datos['VICT_SEX']}, {arma}
Estado actual del caso: {datos['STATUS_DESC']}
El modelo predictivo estimacon {resolucion}

### Codificacion de Variables Categóricas
```python
fecha=pd.to_datetime(df["DATE OCC"], errors="coerce")
df["YEAR OCC"]=fecha.dt.year
df["MONTH OCC"]=fecha.dt.month
df["DAY OCC"]=fecha.dt.day
df=df.drop("DATE OCC", axis=1)

df['LOCATION']= encoderLocation.transform(df['LOCATION'])

df['Vict Sex']= encoderVictSex.transform(df['Vict Sex'])

df['Vict Descent']= encoderVictDescent.transform(df['Vict Descent'])

df["Status Desc"]=df["Status Desc"].map(
    {
    "Adult Arrest":1,
    "Juv Arrest":1, 
    "Adult Other":0, 
    "Juv Other":0
    })
```

    
