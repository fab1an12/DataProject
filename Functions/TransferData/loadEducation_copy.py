import pandas as pd
import requests
from io import StringIO
import pg8000

# URL del archivo CSV
url_centros_educativos = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/centros-educativos-en-valencia/exports/csv?lang=es&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

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

def crear_tabla_centros_y_insertar_datos(df, db_config):
    connection = pg8000.connect(**db_config)
    cursor = connection.cursor()

    # Crear la tabla
    create_table_query = """
    CREATE TABLE IF NOT EXISTS centros_educativos (
        latitud VARCHAR(255),
        longitud VARCHAR(255),
        Geo_Point VARCHAR(255),
        Geo_Shape TEXT,
        codcen INT PRIMARY KEY,
        dlibre VARCHAR(255),
        dgenerica VARCHAR(255),
        despecific VARCHAR(255),
        regimen VARCHAR(50),
        direccion VARCHAR(255),
        codpos INT,
        municipio VARCHAR(100),
        provincia VARCHAR(100),
        telef VARCHAR(50),
        fax VARCHAR(50),
        mail VARCHAR(255)
    );
    """
    cursor.execute(create_table_query)

    # Insertar los datos
    insert_query = """
    INSERT INTO centros_educativos (
        latitud, longitud, Geo_Point, Geo_Shape, codcen, dlibre, dgenerica, despecific, regimen,
        direccion, codpos, municipio, provincia, telef, fax, mail
    ) VALUES (
        %s,%s,%s,%s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
    """
    for _, row in df.iterrows():
        geo_point_split = str(row['Geo Point']).split(',')
        latitud = float(geo_point_split[0]) if len(geo_point_split) > 1 else None
        longitud = float(geo_point_split[1]) if len(geo_point_split) > 1 else None

        cursor.execute(insert_query, (
            longitud,
            latitud,
            row['Geo Point'],
            row['Geo Shape'],
            int(row['codcen']),
            row['dlibre'],
            row['dgenerica_'],
            row['despecific'],
            row['regimen'],
            row['direccion'],
            int(row['codpos']),
            row['municipio_'],
            row['provincia_'],
            row['telef'],
            row['fax'],
            row['mail']
        ))

    connection.commit()
    print("Datos insertados correctamente.")

    cursor.close()
    connection.close()

# Verificar o crear la base de datos
verificar_o_crear_base_datos(SERVER_CONFIG, DB_NAME)

# Descargar el CSV y procesar los datos
df_centros = descargar_csv_a_df(url_centros_educativos)

if df_centros is not None:
    # Crear tabla y cargar datos en la base de datos
    crear_tabla_centros_y_insertar_datos(df_centros, DB_CONFIG)