# Pipeline de ETL para Análisis y Control de Cobranzas

Proyecto Final presentado en el marco del BootCamp de Data Analyst Full Program otorgado por Unicorn Academy [https://unicornacademy.es/](https://unicornacademy.es/)
<hr />

## 🎙️ Presentación
Este proyecto pretende exponer como una problemática real y concreta relacionada con la manipulación de datos que enfrenta una empresa en el desarrollo de sus operaciones habituales, puede ser resuelta satisfactoriamente combinando con buen criterio la gestión de flujo de trabajo y el empleo de herramientas adecuadas.
<hr />

## ❌ Problemática

Una compañía percibe sus ingresos por comisiones sobre cobranzas realizadas, sin realizar controles sobre la correcta liquidación de esas comisiones. Esto se debe a que la fuente de datos consiste en varios archivos excel sin formato tabular limpio, de un tamaño que tornan difícil su manipulación manual con herramientas convencionales y que a su vez requieren tareas de gestión de datos complejas.
<hr />

## 💡 Propuesta

Resolver la problemática orquestando un pipeline de ETL de datos con python. El mismo recorre un directorio específico (este repositorio), recupera archivos .xls, los manipula y unifica en un solo dataframe final. Luego, ejecuta scripts SQL que definen la estructura de la BD e ingesta los datos en MySQL. Primero en una tabla utilizada como “landing”, para luego moverlos dentro del DWH emulando una arquitectura medallion, finalizando en vistas accesibles para los usuarios. Por último conecta Power BI Desktop a la BD para consumir los datos. 

El archivo PBI, fue diseñado con: parámetros dinámicos de conexión a MySQL, modelo de datos estrella, diversas medidas DAX y representaciones gráficas. El archivo se dispone con formato PBI Template. Todo con la idea de brindar a esta herramienta la función analítica del proyecto.
<hr />

## 🛠️ Stack Tecnológico - Requisitos Previos
- [x] **Windows** (OS).
- [x] **Python 3.9+** (se recomienda el uso de Jupyter Notebook - Anaconda).
- [x] **MySQL Server 8.0+** y **Connector/NET 8.0.33** (funcionando localmente) .
- [x] **Power BI Desktop** (visualización).
<hr />

## ⚠️ Ejecución
> [!IMPORTANT]  
> Siga estos pasos para reproducir el pipeline en su entorno local:

1. Descargue todos los archivos de la carpeta ‘**descargas**’ en el mismo directorio local.
2. Modifique el archivo ‘**.env.ejemplo**’ con sus credenciales de acceso a MySQL, y luego renombre el archivo a ‘**.env**’
3. Ejecute el archivo de Jupyter Notebook ‘**PI_UA_orquestador.ipynb**’.
   * Importante: Ejecutar este archivo dentro del mismo directorio (carpeta) donde se descargaron los archivos del punto 1.
4. El flujo finaliza inicializando el template de Power BI para visualizar los resultados.
<hr />

## 🗂️ Estructura del Proyecto

```text
pipeline_analisis_de_cobranzas/
│
├── sql/                                 # Scripts SQL
│   ├── 1_PU_UA_DDL.sql                    # Define estructura de BDs
│   ├── 2_PU_UA_inserts.sql                # Ingesta datos en BDs
│   ├── 3_PU_UA_SO_calendario.sql          # Crea SP de para tabla dim "calendario"
│   ├── 4_PU_UA_capa_dos_vistas.sql        # Crea vistas para consumo final
│
├── data/                                # Datasets del proyecto
│   ├── cruda/                             # Archivos .xls en crudo
|   └── limpia/                            # Archivo .csv final
│
├── descargas/                           # Archivos para descargar
│   ├── .env.ejemplo                        # ejemplo de variables de entorno MySQL (se debe renombrar a .env)
│   └── PI_UA_analisis_cobranzas.pbit       # Template para Power BI Desktop
│   └── PI_UA_orquestador.ipynb             # Archivo orquestador del pipeline
│
├── modulos/                             # Modulos del código fuente
│   ├── carga.py                            # Funciones para ingesta de datos en MySQL
│   └── extraccion.py                       # Funciones para extraer y unificar datos
│   └── transformacion.py                   # Funciones para normalizar datos
│
├── README.md                            # Presentación e intrucciones importantes
│
└── requirements.txt                     # Dependencias (instala automaticamente el orquestador)
```
<hr />

## 🖊️ Autor
Marcelo F. Martin - Contador Público & Analista de Datos

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](http://www.linkedin.com/in/marcelo-f-martin)
