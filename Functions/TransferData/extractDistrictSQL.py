import psycopg2
import json
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def extraer_barrios_sql():
    connection = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT nombre, geo_shape FROM distritos"
            cursor.execute(query)
            
            barrios_lista = []
            for row in cursor.fetchall():
                nombre, geo_shape = row
                # Parsear el campo geo_shape desde JSON
                geo_shape_dict = json.loads(geo_shape)
                coordenadas = geo_shape_dict["coordinates"]
                barrios_lista.append({"nombre": nombre, "coordenadas": coordenadas})
                
            return barrios_lista
    finally:
        connection.close()

# Llamada a la función
barrios = extraer_barrios_sql()
print(barrios)