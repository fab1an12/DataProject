# **Recomendador de Distritos en Valencia**

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
   -[Precios de alquiler por m<sup>2</sup>](https://valencia.opendatasoft.com/explore/dataset/precio-alquiler-vivienda/table/)
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
   cd Functions
   ```

2. **Configurar el entorno Python**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Iniciar los contenedores de Docker**
   ```bash
   docker-compose up --build
   ```

## 5. Uso del Proyecto
