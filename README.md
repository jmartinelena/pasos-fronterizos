# Pipeline en Airflow para extraer la información de los [pasos fronterizos argentinos](https://www.argentina.gob.ar/seguridad/pasosinternacionales)

Proyecto de ingeniería de datos donde se scrapea información de los 10 pasos fronterizos argentinos más utilizados, según [los ingresos y egresos de personas al país durante 2019](https://www.datos.gob.ar/dataset/interior-ingresos-egresos-personas-al-pais-residencias-otorgadas), y se los almacena en una base de datos en MySQL mediante un DAG en Airflow.  
Los pasos fronterizos involucrados son:  
- [Salvador Mazza - Yacuiba](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/22/Salvador-Mazza-Yacuiba)
- [Puerto Chalanas - Bermejo](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/24/Puerto-Chalanas-Bermejo)
- [Gualeguaychú - Fray Bentos](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/4/Gualeguaych%C3%BA-Fray-Bentos)
- [La Quiaca - Villazón](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/18/La-Quiaca-Villaz%C3%B3n)
- [Aguas Blancas - Bermejo](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/23/Aguas-Blancas-Bermejo)
- [Bernardo de Irigoyen - Dionisio Cerqueira](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/12/Bernardo-de-Irigoyen-Dionisio-Cerqueira)
- [Sistema Cristo Redentor](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/29/Sistema-Cristo-Redentor)
- [Paso de los Libres - Uruguayana](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/73/Paso-de-los-Libres-Uruguayana)
- [Cardenal Antonio Samoré](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/42/Cardenal-Antonio-Samor%C3%A9)
- [Puerto Colon - Puerto Paysandu](https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/rio/82/Puerto-Colon-Puerto-Paysandu")

## Cómo levantar el proyecto

Es necesario tener instalado [Docker](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/).  
1. Crear las carpetas `dags`, `logs` y `plugins` en la carpeta donde se vaya a levantar el proyecto. Mas información para linux: [acá](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user). 
2. Ejecutar `docker compose up -d` en la carpeta donde se vaya a levantar el proyecto (y donde esté el archivo docker-compose.yaml). Para supervisar como se van levantando los recursos se puede ejecutar `docker compose logs -f`.
3. Una vez se hayan creado e inicializado los recursos, se puede acceder a la UI web en localhost:8080 (por defecto) y loggearse con el usuario y contraseña definidos en docker-compose.yaml (por defecto tanto el usuario como la contraseña son "airflow").

En la interfaz web se puede ejecutar y supervisar el DAG `pasos_fronterizos`. Para dejar de correr el proyecto debe ejecutarse `docker compose down`.

## Descripción del DAG

El DAG se corre cada una hora y comienza por un task group donde se agrupan las tasks para preparar la base de datos. En este task group se crean las tablas necesarias, se les asigna los constraints necesarios y se agrega un stored procedure para hacer UPSERT de la información scrapeada de cada paso. Luego, en paralelo se extrae la información de cada paso fronterizo y esta se almacena en la base de datos MySQL que se inicializo junto a Airflow al levantar el proyecto con docker compose.  
Si el sistema que provee la información de pasos fronterizos esta caído, como es el caso al momento de escribir esto, y no está disponible la información para algún paso se saltan las taks de extracción y carga para ese paso, como puede verse en la siguiente imagen, donde hay un solo paso "en línea" y los demás no están disponibles:    

![Composición del DAG](https://i.imgur.com/e2N5rWr.png)

## Estructura de la base de datos

La base de datos se diseñó bajo un modelo en estrella, donde la tabla de pasos fronterizos es la tabla de hechos (o fact table), y tiene como dimensiones la fecha, la locación del paso y las propiedades del paso en ese instante (ej.: temperatura, visibilidad, etc).

![Diseño de la base de datos](https://i.imgur.com/rMukWyk.png)