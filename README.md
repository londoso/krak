### Introducción

Para este ejercicio se realizarán capturas de datos desde diferentes fuentes de información de caracter publico, en este caso se importarán archivos planos CSV y JSON directamente desde una base de datos Postgresql. Este ultimo será obtenido a traves de [foraign data wrapper](https://wiki.postgresql.org/wiki/Foreign_data_wrappers "foraign data wrapper") que permite a su vez acceder a metadata externa desde diversos motores de bases de datos.

### Definición de la arquitectura

Los componentes de arquitectura se plantean en su totalidad para la nube de AWS con bases de datos RDS Postgresql, instancias de computo EC2 con Amazon Linux y bucket S3.

### Despliegue de infraestructura

Para el despliegue de toda la infraestructura se cuenta con un archivo de codigo cludformation en formato yaml que automatiza todo el proceso, éste se puede realizar a través de AWS CLI o desde la consola web de AWS como lo veremos a continuación.



### Caso de análisis

The World Bank cuenta con al rededor de 4000 diferentes indicadores que definen el acceso a la educación a nivel mundial. De allí se pueden realizar diferentes analisis pero se deben realizar diferentes procesos como validación de formatos y limpieza de información antes de ser cargada a la base de datos.

##### Modelo de datos

A continuación se presenta el modelo de datos de una tabla en un modelo relacional de Postgresql. Para el caso de uso solo se tomaron desde el dataframe los años 2016 y 2017 para facilidad del proceso pero se podrían tomar más de ser requerido.

| Columna | Tipo de dato | No nulo | PK  |
| ------------ | ------------ | ------------ | ------------ |
| Country Name | varchar(80)  | Si |   |
| Indicator Name  | varchar(200) | Si |   |
| year  | integer(4)  |   |   |
| value  | decimal(10,10) |   |  |


Como mejora al modelo se podría plantear a futuro tener la información en campos tipo JSON, lo cual permite tener una mejor compresión en el tamaño de las tablas.

modelo de datos xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Como la fuente de datos CSV se encuentran los años en modo de columna, se debe aplicar la función melt() para realizar el proceso de "unpivot". De esta forma se podría almacenar la información en una base de datos relacional para su posterior análisis.

[![Dataframe Head](https://drive.google.com/uc?export=view&id=1BcboBdvVWYUP1tTm7U6CI_p8-0fAi0H9 "Dataframe Head")](https://drive.google.com/file/d/1BcboBdvVWYUP1tTm7U6CI_p8-0fAi0H9/view?usp=sharing "Dataframe Head")

Lo primero que se debe aplicar es la función melt(), con esta se garantiza que tenemos la información de acuerdo al modelo de la tabla definido en el modelo de datos previamente. 

[![Melt head](https://drive.google.com/uc?export=view&id=17XiAjxunulpeL35TK_dRYEqlvSC61tze "Melt head")](https://drive.google.com/file/d/17XiAjxunulpeL35TK_dRYEqlvSC61tze/view?usp=sharing "Melt head")



### Fuentes de Información

- [THE WORLD BANK | Education Statistics (Formato CSV)](https://datacatalog.worldbank.org/dataset/education-statistics "THE WORLD BANK | Education Statistics (Formato CSV)")

# Editor.md

![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)
