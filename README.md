## Introducción

Para este ejercicio se realizarán capturas de datos desde diferentes fuentes de información de caracter publico, en este caso se importarán archivos planos CSV y JSON directamente desde una base de datos Postgresql. Este ultimo será obtenido a traves de [foraign data wrapper](https://wiki.postgresql.org/wiki/Foreign_data_wrappers "foraign data wrapper") que permite a su vez acceder a metadata externa desde diversos motores de bases de datos.

## Definición de la arquitectura

Los componentes de arquitectura se plantean en su totalidad para la nube de AWS con bases de datos RDS Postgresql, instancias de computo EC2 con Amazon Linux y bucket S3.

[![Diagrama de Arquitectura](https://github.com/londoso/krak/blob/main/IMG/arquitectura.png "Diagrama de Arquitectura")](https://github.com/londoso/krak/blob/main/IMG/arquitectura.png "Diagrama de Arquitectura")

## Despliegue de infraestructura

Para el despliegue de toda la infraestructura se cuenta con un archivo de codigo cludformation en formato yaml que automatiza todo el proceso, éste se puede realizar a través de AWS CLI o desde la consola web de AWS como lo veremos a continuación.

En gran medida se hace uso de la capa gratuita para cada uno de los servicios y dura aproximadamente 16 minutos el despliegue de toda la infraestructura.

El archivo puede ser obtenido clonando este repositorio en la ruta /CF/template.yaml o descargandolo desde el siguiente enlace.

https://raw.githubusercontent.com/londoso/krak/main/CF/template.yaml

Se inicia creando una llave en formato .PEM, la cual permitirá el acceso de forma segura a la instancia EC2 Linux. En este caso se llamará "krak".

[![](https://github.com/londoso/krak/blob/main/IMG/key2.jpg)](https://github.com/londoso/krak/blob/main/IMG/key2.jpg)

Se crea un nuevo stack e invoca el archivo template.yaml 

[![](https://github.com/londoso/krak/blob/main/IMG/ima1.jpg)](https://github.com/londoso/krak/blob/main/IMG/ima1.jpg)

Luego ingresa un nombre para el stack, en este caso "krak" pero puede ser cualquier nombre. Los demás parámetros se pueden dejar iguales.

[![](https://github.com/londoso/krak/blob/main/IMG/ima2.jpg)](https://github.com/londoso/krak/blob/main/IMG/ima2.jpg)

En la siguiente ventana "Configure stack options" no se modifica nada para este caso.

[![](https://github.com/londoso/krak/blob/main/IMG/ima3.jpg)](https://github.com/londoso/krak/blob/main/IMG/ima3.jpg)

En la última ventana se hace una revisión completa del stack. Al final en la sección "Capabilities" se debe aceptar para que se pueda crear el Role IAM, el cual permitira la conexión entre la instancia EC2 y el bucket S3.

Solo resta iniciar la creación del stack y aproximadamente en 16 minutos quedará desplegada por completo.

[![](https://github.com/londoso/krak/blob/main/IMG/ima4.jpg)](https://github.com/londoso/krak/blob/main/IMG/ima4.jpg)

Cuando finalice en la sección de output podrá encontrar información importante para la conexión como se muestra a continuación.

[![](https://github.com/londoso/krak/blob/main/IMG/out1.jpg)](https://github.com/londoso/krak/blob/main/IMG/out1.jpg)

Para conectarse lo puede hacer con la llave descargada previamente krak.pem y desde una consola con el siguiente comando.

ssh -i "krak.pem" ec2-user@52.90.46.204

## Caso de análisis

The World Bank cuenta con al rededor de 4000 diferentes indicadores que definen el acceso a la educación a nivel mundial. De allí se pueden realizar diferentes analisis pero se deben realizar diferentes procesos como validación de formatos y limpieza de información antes de ser cargada a la base de datos.

#### Modelo de datos

A continuación se presenta el modelo de datos de una tabla en un modelo relacional de Postgresql. Para el caso de uso solo se tomaron desde el dataframe los años 2016 y 2017 para facilidad del proceso pero se podrían tomar más de ser requerido.

| Columna | Tipo de dato | No nulo | PK  |
| ------------ | ------------ | ------------ | ------------ |
| PK | serial  | Si | Si |
| COUNTRYNAME | varchar(80)  | Si |   |
| INDICATORNAME  | varchar(200) | Si |   |
| YEAR  | int | Si |   |
| VALUE  | decimal(3,20) | Si |  |


Como mejora al modelo se podría plantear a futuro tener la información en campos tipo JSON, lo cual permite tener una mejor compresión en el tamaño de las tablas.


Como la fuente de datos CSV se encuentran los años en modo de columna, se debe aplicar la función melt() para realizar el proceso de "unpivot". De esta forma se podría almacenar la información en una base de datos relacional para su posterior análisis.

[![Dataframe Head](https://github.com/londoso/krak/blob/main/IMG/df_head.jpg "Dataframe Head")](https://github.com/londoso/krak/blob/main/IMG/df_head.jpg "Dataframe Head")

Lo primero que se debe aplicar es la función melt(), con esta se garantiza que tenemos la información de acuerdo al modelo de la tabla definido en el modelo de datos previamente. 

[![Melt head](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")



### Fuentes de Información

- [THE WORLD BANK | Education Statistics (Formato CSV)](https://datacatalog.worldbank.org/dataset/education-statistics "THE WORLD BANK | Education Statistics (Formato CSV)")