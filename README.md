## Introducción

Para este ejercicio se realizarán capturas de datos desde diferentes fuentes de información de caracter publico, en este caso se importarán archivos planos CSV y JSON directamente desde una base de datos Postgresql. Este ultimo será obtenido a traves de [foraign data wrapper](https://wiki.postgresql.org/wiki/Foreign_data_wrappers "foraign data wrapper") que permite a su vez acceder a metadata externa desde diversos motores de bases de datos.

Aducionalmente, se hace uso de Python como lenguaje y sus librerias (psycopg2, pandas, os, s3fs).

## Definición de la arquitectura

Los componentes de arquitectura se plantean en su totalidad para la nube de AWS con bases de datos RDS Postgresql, instancias de computo EC2 con Amazon Linux y bucket S3.

[![Diagrama de Arquitectura](https://github.com/londoso/krak/blob/main/IMG/arquitectura.png "Diagrama de Arquitectura")](https://github.com/londoso/krak/blob/main/IMG/arquitectura.png "Diagrama de Arquitectura")

Como se puede observar en el anterior diagrama, se tiene una instancia EC2 que cumple dos labores, la de Bastion Host y Computo. Adicionalmente, se tienen dos RDS Postgresql, la Master para realizar las cargas de datos y la Replica para realizar consultas y servir de insumo para llevar estos datos a otras zonas de datos u análisis.

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

A continuación se presenta el modelo de datos de una tabla en un modelo relacional de Postgresql. Para el caso de uso solo se tomaron desde el dataframe los años 2016 y 2017 por facilidad del proceso pero se podrían cargar más de ser requerido.

| Columna | Tipo de dato | No nulo | PK  |
| ------------ | ------------ | ------------ | ------------ |
| PK | serial  | Si | Si |
| COUNTRYNAME | varchar(80)  | Si |   |
| INDICATORNAME  | varchar(200) | Si |   |
| YEAR  | int |  |   |
| VALUE  | decimal(100,50) | |  |

```sql
CREATE TABLE REPO.INDICADOR (
	PK SERIAL PRIMARY KEY, 
	COUNTRYNAME varchar(80) not null
	, INDICATORNAME varchar(200) not null, YEAR int, 
	VALUE numeric(100,50)
);
```
Se define un campo PK autonumerico, el cual genera automaticamente un índice y puede ser beneficioso al memento de realizar extracciones de datos en paralelo.

Como mejora al modelo se podría plantear a futuro tener la información en campos tipo JSON, lo cual permite tener una mejor compresión en el tamaño de las tablas.

Ya que la fuente de datos CSV se encuentran los años en modo de columna, se debe aplicar la función melt() para realizar el proceso de "unpivot". De esta forma se podría almacenar la información en una base de datos relacional para su posterior análisis.

[![Dataframe Head](https://github.com/londoso/krak/blob/main/IMG/df_head.jpg "Dataframe Head")](https://github.com/londoso/krak/blob/main/IMG/df_head.jpg "Dataframe Head")

Lo primero que se debe aplicar es la función melt(), con esta se garantiza que tenemos la información de acuerdo al modelo de la tabla definido en el modelo de datos previamente. 

[![Melt head](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")

Con la nueva estructura se puede proceder a cargar los datos a la tabla, para ello se hace uso de la función COPY de Postgresql, lo que permite que se inserten los datos de forma masiva en un buen tiempo.

## Ejecución de modelo manualmente

A continuación se describen los pasos para ejecutar el modelo. Luego de que se encuentre la infraestructura disponible, se podrán ejecutar una serie de scripts en Python para sumular el proceso.

1. Preparación del ambiente de base de datos.

En este paso se crea el esquema y la tabla encargada de recibir los datos de los indicadores.

[![](https://github.com/londoso/krak/blob/main/IMG/create_env.jpg)](https://github.com/londoso/krak/blob/main/IMG/create_env.jpg)

```shell
cd ~/krak && git pull
python3 create_env.py
```

2. Carga de archivo CSV.

En este paso se realiza todo el proceso para llevar el archivo desde el Bucket S3 hasta la tabla en la base de datos Postgresql.

- Se crea un Dataframe a partir de un archivo CSV, cargado directamente desde el bucket S3
- Se generan las transformaciones necesarias al Dataframe.
- Se genera un archivo CSV temporal con la estructura definitiva.
- Se carga el archivo temporal a la tabla de indicadores en la base de datos Postgresql. 

[![](https://github.com/londoso/krak/blob/main/IMG/copy_csv.jpg)](https://github.com/londoso/krak/blob/main/IMG/copy_csv.jpg)

```shell
cd ~/krak && git pull
python3 copy_csv.py
```

## Conclusión

Para finalizar se plantean algunas preguntas desde el lado de infraestructura.

- ¿ Qué pasa si los datos se incrementaran en 100x ?

	Desde la máquina EC2 de computo se puede manejar un grupo de autoescalamiento, que permita atender la demanda ya que se deberían procesar más datos. Por parte de la base de datos se puede realizar un escalamiento horizontal, aumentando los recursos de las RDS y vertical, aumentando las replicas de lectura.

- ¿ Qué pasa si las tuberías se ejecutaran diariamente a las 7 de la mañana ?

	No se debería tener impacto ya que los usuarios solo tienen acceso a replicas de lectura de la base de datos, las inserciones se realizan en la RDS Master.

- ¿ Qué pasa si la base de datos necesitara ser accedida por más de 100 personas ?

	Tal como la pregunta anterior, los usuarios solo hacen uso de las replicas de lectura. Si hay problemas de desempeño, se pueden escalar los recursos de las RDS. Para este punto se puede mejorar el proceso de escalamiento con el uso de Aurora Postgresql ya que este servicio maneja autoescalamiento automático.

Desde el punto de análisis del modelo se pueden plantear otras preguntas.

- ¿ Porqué se eligió este modelo ?

	Se elige un modelo datos relaciolal dado a su uso vigente y a que muchas herramientas se encuentran optimizadas para este fin. Como mejora al modelo se sugiere migrar a modelos no relacionales, lo cual puede mejorar el rendimiento notablemente.

- ¿ Qué preguntas surgen a partir del análisis del modelo ?

	¿ Cómo se puede segmentar mejor la información ?
	¿ Cuáles son los principales indicadores ?
	¿ Es suficiente la información para realizar un análisis o usar una herramienta de visualización de datos ?


## Fuentes de Información

- [THE WORLD BANK | Education Statistics (Formato CSV)](https://datacatalog.worldbank.org/dataset/education-statistics "THE WORLD BANK | Education Statistics (Formato CSV)")