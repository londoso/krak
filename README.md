## Introducción

Para este ejercicio se realizarán capturas de datos desde diferentes fuentes de información de caracter publico, en este caso se importarán archivos planos CSV y JSON directamente desde una base de datos Postgresql. Este ultimo será obtenido a traves de [foraign data wrapper](https://wiki.postgresql.org/wiki/Foreign_data_wrappers "foraign data wrapper") que permite a su vez acceder a metadata externa desde diversos motores de bases de datos.

## Definición de la arquitectura

Los componentes de arquitectura se plantean en su totalidad para la nube de AWS con bases de datos RDS Postgresql, instancias de computo EC2 con Amazon Linux y bucket S3.

[![Diagrama de Arquitectura](https://drive.google.com/uc?export=view&id=1F_d0DOoDcITkQNQyn1O0QKl5OK5vZf9s "Diagrama de Arquitectura")](https://drive.google.com/file/d/1F_d0DOoDcITkQNQyn1O0QKl5OK5vZf9s/view?usp=sharing "Diagrama de Arquitectura")

## Despliegue de infraestructura

Para el despliegue de toda la infraestructura se cuenta con un archivo de codigo cludformation en formato yaml que automatiza todo el proceso, éste se puede realizar a través de AWS CLI o desde la consola web de AWS como lo veremos a continuación.

En gran medida se hace uso de la capa gratuita para cada uno de los servicios y dura aproximadamente 16 minutos el despliegue de toda la infraestructura.

El archivo puede ser obtenido clonando este repositorio en la ruta /CF/template.yaml o descargandolo desde el siguiente enlace.

https://raw.githubusercontent.com/londoso/krak/main/CF/template.yaml

Se inicia creando una llave en formato .PEM, la cual permitirá el acceso de forma segura a la instancia EC2 Linux. En este caso se llamará "krak".

[![](https://drive.google.com/uc?export=view&id=1oUUl5jee0yZX1DkeyJvB8_win3g9NVP-)](https://drive.google.com/file/d/1oUUl5jee0yZX1DkeyJvB8_win3g9NVP-/view?usp=sharing)

Se crea un nuevo stack e invoca el archivo template.yaml 

[![](https://drive.google.com/uc?export=view&id=15V0K-4OGzHnPrSDB_f_g-GsrlxaW4q3z)](https://drive.google.com/file/d/15V0K-4OGzHnPrSDB_f_g-GsrlxaW4q3z/view?usp=sharing)

Luego ingresa un nombre para el stack, en este caso "krak" pero puede ser cualquier nombre. Los demás parámetros se pueden dejar iguales.

[![](https://drive.google.com/uc?export=view&id=1ZMU7WDt7nlPaP3aX16Sfqo6jdkaxzc1-)](https://drive.google.com/file/d/1ZMU7WDt7nlPaP3aX16Sfqo6jdkaxzc1-/view?usp=sharing)

En la siguiente ventana "Configure stack options" no se modifica nada para este caso.

[![](https://drive.google.com/uc?export=view&id=1IsZDvA7hP_m-zua6G0vC6SkI4wQoTjxJ)](https://drive.google.com/file/d/1IsZDvA7hP_m-zua6G0vC6SkI4wQoTjxJ/view?usp=sharing)

En la última ventana se hace una revisión completa del stack. Al final en la sección "Capabilities" se debe aceptar para que se pueda crear el Role IAM, el cual permitira la conexión entre la instancia EC2 y el bucket S3.

Solo resta iniciar la creación del stack y aproximadamente en 16 minutos quedará desplegada por completo.

[![](https://drive.google.com/uc?export=view&id=1eAZH2hWBLoewGOJuIDY53FND3YbxZcBj)](https://drive.google.com/file/d/1eAZH2hWBLoewGOJuIDY53FND3YbxZcBj/view?usp=sharing)

Cuando finalice en la sección de output podrá encontrar información importante para la conexión como se muestra a continuación.

[![](https://drive.google.com/uc?export=view&id=1c9f1yNU0__gDxGfe2si9M-DSo2-55db8)](https://drive.google.com/file/d/1c9f1yNU0__gDxGfe2si9M-DSo2-55db8/view?usp=sharing)

Para conectarse lo puede hacer con la llave descargada previamente krak.pem y desde una consola con el siguiente comando.

ssh -i "krak.pem" ec2-user@52.90.46.204

## Caso de análisis

The World Bank cuenta con al rededor de 4000 diferentes indicadores que definen el acceso a la educación a nivel mundial. De allí se pueden realizar diferentes analisis pero se deben realizar diferentes procesos como validación de formatos y limpieza de información antes de ser cargada a la base de datos.

#### Modelo de datos

A continuación se presenta el modelo de datos de una tabla en un modelo relacional de Postgresql. Para el caso de uso solo se tomaron desde el dataframe los años 2016 y 2017 para facilidad del proceso pero se podrían tomar más de ser requerido.

| Columna | Tipo de dato | No nulo | PK  |
| ------------ | ------------ | ------------ | ------------ |
| Country Name | varchar(80)  | Si |   |
| Indicator Name  | varchar(200) | Si |   |
| year  | integer(4)  |   |   |
| value  | decimal(10,10) |   |  |


Como mejora al modelo se podría plantear a futuro tener la información en campos tipo JSON, lo cual permite tener una mejor compresión en el tamaño de las tablas.


Como la fuente de datos CSV se encuentran los años en modo de columna, se debe aplicar la función melt() para realizar el proceso de "unpivot". De esta forma se podría almacenar la información en una base de datos relacional para su posterior análisis.

[![Dataframe Head](https://drive.google.com/uc?export=view&id=1BcboBdvVWYUP1tTm7U6CI_p8-0fAi0H9 "Dataframe Head")](https://drive.google.com/file/d/1BcboBdvVWYUP1tTm7U6CI_p8-0fAi0H9/view?usp=sharing "Dataframe Head")

Lo primero que se debe aplicar es la función melt(), con esta se garantiza que tenemos la información de acuerdo al modelo de la tabla definido en el modelo de datos previamente. 

[![Melt head](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")](https://github.com/londoso/krak/blob/main/IMG/melt_count.jpg "Melt head")



### Fuentes de Información

- [THE WORLD BANK | Education Statistics (Formato CSV)](https://datacatalog.worldbank.org/dataset/education-statistics "THE WORLD BANK | Education Statistics (Formato CSV)")