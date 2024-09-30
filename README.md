# prueba_celsia

Este proyecto implementa una técnica de clusterización sobre datos de circuitos eléctricos para detectar grupos con comportamientos similares en cuanto a la media de duración de las llamadas y el porcentaje de clientes que llamaron. Utiliza Python y una base de datos SQLite para la extracción de datos y análisis.

## Contenidos del Proyecto

- **main.py**: Archivo principal que ejecuta el análisis, el clustering y genera los resultados.
- **db.py**: Archivo de soporte para la conexión y carga de datos desde una base de datos SQLite.
- **resultado_final.xlsx**: Archivo generado al final del análisis que contiene las métricas y clusters resultantes.
  
## Instrucciones de Ejecución

### Prerrequisitos

- Tener instalado Python 3.x
- Tener instalado Docker si prefieres usar contenedores
- Instalar las dependencias del proyecto descritas en el archivo `requirements.txt`
- Tener disponible una base de datos SQLite con las tablas `incidencias_duracion` y `llamadas`.

 ```bash
docker build -t clustering-circuitos .
docker run -v $(pwd):/app clustering-circuitos
 ```
Estructura de los archivos

 ```bash
├── Dockerfile            # Archivo de configuración para Docker
├── main.py               # Script principal del proyecto
├── db.py                 # Módulo de conexión y carga de datos desde la base de datos
├── requirements.txt      # Lista de dependencias para el proyecto
├── README.md             # Este archivo de instrucciones
├── resultado_final.xlsx  # Archivo Excel generado con los resultados del análisis
