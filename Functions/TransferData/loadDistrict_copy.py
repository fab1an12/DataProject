import pandas as pd
import requests
from io import StringIO
import pg8000

# URL del archivo CSV
url = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/districtes-distritos/exports/csv?lang=es&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

# Configuración de la conexión inicial para el servidor
SERVER_CONFIG = {
    "database": "postgres",
    "user": "postgres",
    "password": "Welcome01",
    "host": "localhost",
    "port": 5432
}

# Configuración para la nueva base de datos
DB_NAME = "dataproject"
DB_CONFIG = {
    "database": DB_NAME,
    "user": "postgres",
    "password": "Welcome01",
    "host": "localhost",
    "port": 5432
}

def verificar_o_crear_base_datos(server_config, db_name):
    connection = pg8000.connect(**server_config)
    connection.autocommit = True
    cursor = connection.cursor()

    # Verificar si la base de datos existe
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (db_name,)
    )
    if not cursor.fetchone():
        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Base de datos '{db_name}' creada.")
    else:
        print(f"La base de datos '{db_name}' ya existe.")

    cursor.close()
    connection.close()

def descargar_csv_a_df(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, sep=';')
        return df
    except Exception as e:
        print(f"Error al descargar o procesar el CSV: {e}")
        return None

def crear_tabla_y_insertar_datos(df, db_config):
    connection = pg8000.connect(**db_config)
    cursor = connection.cursor()

    # Crear la tabla
    create_table_query = """
    CREATE TABLE IF NOT EXISTS distritos (
        id SERIAL PRIMARY KEY,
        objectid INT,
        nombre VARCHAR(255),
        codigo_distrito INT,
        area FLOAT,
        geo_shape TEXT,
        geo_point_2d VARCHAR(255),
        latitud FLOAT,
        longitud FLOAT
    );
    """
    cursor.execute(create_table_query)

    # Insertar los datos
    insert_query = """
    INSERT INTO distritos (objectid, nombre, codigo_distrito, area, geo_shape, geo_point_2d, latitud, longitud)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    for _, row in df.iterrows():
        geo_point_split = str(row['geo_point_2d']).split(',')
        latitud = float(geo_point_split[0]) if len(geo_point_split) > 1 else None
        longitud = float(geo_point_split[1]) if len(geo_point_split) > 1 else None

        # Ejecutar la inserción
        cursor.execute(insert_query, (
            int(row['objectid']),
            row['Nombre'],
            int(row['Código distrito']),
            float(row['gis.gis.DISTRITOS.area']),
            row['geo_shape'],
            row['geo_point_2d'],
            latitud,
            longitud
        ))

    # Confirmar los cambios
    connection.commit()
    print("Datos insertados correctamente.")

    # Cerrar la conexión
    cursor.close()
    connection.close()

# Verificar o crear la base de datos
verificar_o_crear_base_datos(SERVER_CONFIG, DB_NAME)

# Descargar el CSV y procesar los datos
df = descargar_csv_a_df(url)

if df is not None:
    # Crear tabla y cargar datos en la base de datos
    crear_tabla_y_insertar_datos(df, DB_CONFIG)