# proy-geopostalcode

* Explicación de la solución

Se crea un servicio API con Python y FastApi para cargar un archivo plano con información de ubicaciones Latitud y Longitud a la BD, en el mismo servicio se    realizan el consumo del API localizada en https://postcodes.io para completar el dato del código postal más cercano a cada punto geográfico. El consumo del Api https://postcodes.io se realiza por ciclos de 100 puntos geográficos ya que tiene esta limitante y se van almacenando en la BD, los códigos postales que no logra identificar son almacenados con el valor por defecto "NOT FOUND". Al finalizar la ejecución el servicio construido retorna un JSON con los puntos geográficos a los cuales el API https://postcodes.io no les logró identificar el código postal.

* La solución realizada tiene como arquitectura la creación de dos imágenes docker la primera contiene la aplicación construida con Python y la segunda la BD creada en MySQL

![](https://github.com/ajcas/proy-geopostalcode/blob/main/Arq.png)




* Herramientas utilizadas

    - Python(FastAPI, Pandas, Requests)
    - MySQL
    - Docker
    - VisualStudioCode


* Consideraciones para el despliegue:

    1. El despliegue de la aplicación se realiza por medio del archivo docker-compose.yml
    2. El acceso al API construido es por medio de la url http://localhost/docs
    3. El archivo utilizado para las pruebas es el postcodesgeo10000.csv
    4. La base de datos donde se carga la información se encuentra en localhost:3306 BD local_db, se tienen dos tablas geoloaded(información sin procesar y            geoprocessed(información procesada con el código postal).
    5. 
