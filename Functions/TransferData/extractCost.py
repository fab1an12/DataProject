import os
import pandas as pd
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Configuración de MongoDB
uri = "mongodb+srv://fabianmiulescu:DataProject2024@cluster0.dzrgu.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, server_api=ServerApi('1'))

# Probar la conexión
try:
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")
    exit()

# Base de datos
db = client["precios_vivienda"]

# Lista de barrios
barrios = [
    "algiros", "benicalap", "benimaclet", "camins-al-grau", "campanar", "ciutat-vella",
    "el-pla-del-real", "extramurs", "jesus", "leixample", "lolivereta", "la-saidia",
    "patraix", "poblats-maritims", "quatre-carreres", "rascanya"
]

# Carpeta donde están los archivos HTML
input_folder = "~/Documents/MDA/DataProject/Data/Cost/Ventas"

# Procesar cada barrio
for barrio in barrios:
    # Ruta al archivo HTML
    file_path = os.path.expanduser(os.path.join(input_folder, f"{barrio}.html"))
    
    try:
        # Leer y analizar el archivo HTML
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Buscar la tabla
        table = soup.find('table', {'class': 'js-scroll-header component-table table'})
        if not table:
            print(f"¡Tabla no encontrada para {barrio}!")
            continue
        
        # Extraer encabezados
        headers = [header.text.strip() for header in table.find_all('th')]
        
        # Extraer filas
        rows = [
            {headers[i]: cell.text.strip() for i, cell in enumerate(row.find_all('td'))}
            for row in table.find_all('tr') if row.find_all('td')
        ]
        
        # Insertar datos en la colección correspondiente
        collection = db[barrio]
        if rows:
            collection.insert_many(rows)
            print(f"Datos insertados en la colección '{barrio}'")
        else:
            print(f"No se encontraron datos para insertar en '{barrio}'")

    except Exception as e:
        print(f"Error procesando {barrio}: {e}")

print("¡Proceso completado!")
