import pandas as pd
import numpy as np
from pymongo import MongoClient

def calculate_ahp_weights(uri, database_name, barrios, year=2024):
    # Conexión a MongoDB
    client = MongoClient(uri)
    db = client[database_name]

    # Lista para almacenar los costos medios de cada barrio
    avg_prices = []

    # Iterar sobre los barrios
    for barrio in barrios:
        collection = db[barrio]
        data = list(collection.find({}, {"_id": 0}))  # Excluir _id
        
        if not data:
            print(f"No se encontraron datos para el barrio '{barrio}'.")
            continue

        # Crear un DataFrame con los datos del barrio
        df = pd.DataFrame(data)
        df = df[df['Mes'].str.contains(str(year), na=False)]
        df['Precio m2'] = (
            df['Precio m2']
            .str.replace('€/m2', '', regex=False)
            .str.replace('.', '', regex=False)
            .replace(['n.d.', 'nd'], None)
            .astype(float)
        )
        df = df.dropna(subset=['Precio m2'])

        # Calcular el precio medio del metro cuadrado
        avg_price = df['Precio m2'].mean()
        avg_prices.append(avg_price)

    # Verificar si se encontraron precios
    if not avg_prices:
        raise ValueError("No se encontraron precios válidos para calcular los pesos AHP.")

    # Crear la matriz de comparación por pares
    matrix = np.zeros((len(avg_prices), len(avg_prices)))
    for i in range(len(avg_prices)):
        for j in range(len(avg_prices)):
            matrix[i, j] = avg_prices[i] / avg_prices[j]

    # Normalizar la matriz
    normalized_matrix = matrix / matrix.sum(axis=0)

    # Calcular los pesos AHP
    weights = normalized_matrix.mean(axis=1)

    return weights