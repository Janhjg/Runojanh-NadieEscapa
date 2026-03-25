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
    