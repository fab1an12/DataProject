# **Encuentra tu Distrito Ideal en Valencia**

> *Una herramienta basada en AHP para encontrar el distrito ideal en Valencia según las preferencias del usuario.*

---

### **1. Descripción del Proyecto**

Este proyecto utiliza el Proceso Analítico Jerárquico (AHP) para recomendar los mejores distritos de Valencia basándose en las preferencias del usuario, como precio, servicios, espacios verdes y transporte público. Las recomendaciones se visualizan de forma interactiva mediante Streamlit.

### **Propósito del Proyecto**
La ciudad de Valencia está experimentando un aumento significativo en los precios de alquiler y compra de viviendas. Este programa busca proporcionar una herramienta útil para las personas que necesitan tomar decisiones informadas sobre dónde vivir, considerando no solo los precios actuales, sino también factores como servicios, transporte y calidad de vida en los distritos. 


### **Características Principales**
- **Entrada del Usuario**:  
  El usuario puede indicar sus preferencias en:  
  - Tipo de vivienda (alquiler o compra).  
  - Acceso a servicios (hospitales, centros educativos).  
  - Cantidad de espacios verdes.  
  - Opciones de transporte público.  

- **Procesamiento de Datos**:  
  - Se integra información de Open Data Valencia y OpenMaps.  
  - Los datos se limpian y se estructuran para almacenarlos en una base de datos PostgreSQL.  

- **Visualización**:  
  - Muestra en un mapa interactivo los 3 mejores distritos según las preferencias del usuario.

---

## **2. Fuentes de Datos**
1. **Open Data Valencia**  
   - [Distritos](https://valencia.opendatasoft.com/explore/dataset/districtes-distritos/table/)  
   - [Localización de centros de salud](https://valencia.opendatasoft.com/explore/dataset/hospitales/table/)
   - [Localización de centros educativos](https://valencia.opendatasoft.com/explore/dataset/centros-educativos-en-valencia/table/)
   - [Información sobre transporte público (EMT y Metrovalencia)](https://valencia.opendatasoft.com/explore/dataset/transporte-barrios/table/)
   - [Precios de alquiler por m<sup>2</sup>](https://valencia.opendatasoft.com/explore/dataset/precio-alquiler-vivienda/table/)
   - [Precios de compra por m<sup>2</sup>](https://valencia.opendatasoft.com/explore/dataset/precio-de-compra-en-idealista/table/)
  

2. **OpenMaps**  
   - [Web Scrapping sobre cantidad de espacios verdes por distrito de Valencia](https://www.openstreetmap.org/#map=12/39.4780/-0.4237&layers=P)

---

## **3. Estructura del Proyecto**
```shell
📦 DataProject
 ├── 📂 Data │ 
    ├── Distritos_CodigosPostales.csv │ 
 ├── 📂 Functions │ 
    ├──📂 ManageData │ 
        ├── extractDistrict.py 
        ├── extractParkFromOPMS.py │ 
        ├── LoadDistrict.py │ 
        ├── LoadEducation.py |
        ├── LoadGreenArea.py │ 
        ├── LoadHospitals.py |
        ├── LoadPostalCode.py |
        ├── LoadRentPrice.py 
        ├── LoadSalesPrice.py 
        ├── LoadTransport.py │ 
    ├── calcular_ahp.py 
    ├── createTop3Polygons.py
    ├── greenZonesMatrix.py
    ├── main.py
    ├── PublicServiesMatrix.py
    ├── querys.py 
    ├── rentCostMatrix.py
    ├── salesCostMatrix.py
 ├── docker-compose.yml
 ├── dockerfile
 ├── entrypoint.sh
 ├── querys.sql
 ├── README.md #Documentación
 ├── requirements.txt # Dependencias de Python

```

## **4. Cómo Empezar**

### **4.1. Requisitos Previos**
Asegúrate de tener instalado lo siguiente:
- **Python** (versión 3.9 o superior).  
- **Docker** (incluyendo Docker Compose).

### **4.2. Instalación**
1. **Clonar el repositorio**:
   ```bash
   git clone <https://github.com/fab1an12/DataProject.git>
   ```


2. **Iniciar los contenedores de Docker**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la aplicación**:
4. ```bash
   Una vez que los contenedores estén listos, abre tu navegador y accede a:
   http://localhost:8501
   ```

## **5. Uso del Proyecto**

### **Flujo del Usuario**
1. Abre el navegador y accede a [http://localhost:8501](http://localhost:8501) después de ejecutar el comando `docker-compose up --build`.  
2. En la interfaz de Streamlit, selecciona tus preferencias:  
   - **Tipo de vivienda**: Alquiler o Compra.  
   - Ajusta los pesos relativos para las siguientes variables:  
     - **Coste**: Importancia del coste por metro cuadrado.  
     - **Servicios**: Proximidad a hospitales y centros educativos.  
     - **Zonas verdes**: Cantidad de espacios verdes en el distrito.  
     - **Transporte público**: Disponibilidad de autobuses y metro.  
3. Haz clic en el botón para generar las recomendaciones.  
4. Visualiza en el mapa interactivo los 3 distritos ideales según tus preferencias.


---

## **6. Flujo de Datos**

El flujo del programa sigue los siguientes pasos:

### **Extracción y Carga de Datos**
Los datos iniciales se obtienen de diversas fuentes y se procesan mediante los scripts en la carpeta `ManageData`. Estas son las funciones principales:

1. **Cargar distritos y coordenadas**:  
   - `extractDistrict.py`: Selecciona los nombres y coordenadas de los distritos desde PostgreSQL y los formatea para visualización en Streamlit.

2. **Cargar datos de zonas verdes**:  
   - `extractParkFromOPMS.py`: Obtiene el nombre del distrito y realiza un conteo del número de zonas verdes presentes en cada distrito.

3. **Scripts de carga (`Load*.py`)**:  
   Cada uno de estos scripts toma datos específicos de las fuentes (Open Data del Ayuntamiento de Valencia o Open Maps) y realiza tres pasos clave:  
   - Crea una tabla en PostgreSQL.  
   - Limpia y estructura los datos.  
   - Carga los datos en PostgreSQL.  

   Los datos gestionados incluyen:  
   - **Distritos y códigos postales**: `LoadDistrict.py` y `LoadPostalCode.py`.  
   - **Servicios públicos**: `LoadEducation.py` (centros educativos) y `LoadHospitals.py` (hospitales).  
   - **Zonas verdes**: `LoadGreenArea.py`.  
   - **Transporte**: `LoadTransport.py` (EMT y Metrovalencia).  
   - **Costes de vivienda**: `LoadRentPrice.py` (alquiler) y `LoadSalesPrice.py` (compra).  

---

### **Cálculo AHP**
Una vez que los datos están en PostgreSQL, se procesan para generar matrices AHP específicas para cada variable. Estas son las funciones involucradas:

1. **Matrices AHP por variable**:  
   - `rentCostMatrix.py`: Calcula la matriz de comparación para el coste de alquiler.  
   - `salesCostMatrix.py`: Calcula la matriz de comparación para el coste de compra.  
   - `greenZonesMatrix.py`: Genera la matriz de comparación basada en la cantidad de zonas verdes por distrito.  
   - `PublicServiesMatrix.py`: Crea una matriz de comparación basada en la cantidad de servicios públicos (hospitales y centros educativos) disponibles. 
   - `transportMatrix.py`: Genera la matriz de comparación basada en la cantidad de transportes (EMT y Metrovalencia) disponibles.

2. **Cálculo final del AHP**:  
   - `calcular_ahp.py`: Llama a las matrices de cada variable, las enfrenta usando el método AHP y calcula las ponderaciones finales.  
   - Este script determina el distrito ideal según las preferencias del usuario introducidas en Streamlit.

---

### **Generación de Polígonos y Visualización**
1. **Creación de polígonos para los distritos**:  
   - `createTop3Polygons.py`: Genera polígonos geográficos de los tres mejores distritos seleccionados por el cálculo AHP, listos para mostrarse en el mapa interactivo.

2. **Consulta de datos**:  
   - `querys.py`: Ejecuta consultas específicas a la base de datos PostgreSQL para obtener los datos necesarios en la visualización.

3. **Interfaz de usuario**:  
   - `main.py`: Es el punto de entrada principal del programa.  
     - Recoge las preferencias del usuario mediante controles interactivos en Streamlit.  
     - Muestra los resultados, incluyendo un mapa interactivo con los distritos ideales y sus características.

---
