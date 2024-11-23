from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import locale
import numpy as np

def predict_and_plot_prices(uri, database_name, barrio):
    # Configurar el idioma local a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Conexión a MongoDB
    client = MongoClient(uri)
    db = client[database_name]

    # Obtener los datos del barrio
    collection = db[barrio]
    data = list(collection.find({}, {"_id": 0}))  # Excluir _id
    if not data:
        raise ValueError(f"No se encontraron datos para el barrio '{barrio}'.")

    df = pd.DataFrame(data)

    # Convertir 'Mes' a datetime
    df['Mes'] = pd.to_datetime(df['Mes'], format='%B %Y', errors='coerce')

    # Convertir precios a valores numéricos, manejando 'n.d.'
    df['Precio m2'] = df['Precio m2'].str.replace('€/m2', '').replace('n.d.', None).str.replace('.', '').astype(float)

    # Eliminar filas con valores nulos
    df = df.dropna(subset=['Mes', 'Precio m2'])
    if df.empty:
        raise ValueError(f"Todos los datos de '{barrio}' son inválidos después de eliminar nulos.")

    # Ordenar por fecha
    df = df.sort_values(by='Mes')

    # Crear características adicionales
    df['Año'] = df['Mes'].dt.year
    df['Mes_Num'] = df['Mes'].dt.month

    # Calcular media móvil y variación porcentual
    df['Precio_Media_3M'] = df['Precio m2'].rolling(window=3).mean()
    df['Precio_Variacion'] = df['Precio m2'].pct_change()
    df = df.dropna(subset=['Precio_Media_3M', 'Precio_Variacion'])

    # Definir características y target
    X = df[['Mes_Num', 'Año', 'Precio_Media_3M', 'Precio_Variacion']]
    y = df['Precio m2']

    # Dividir en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Crear datos para predicción futura
    future_data = pd.DataFrame({
        'Mes_Num': [11, 12, 1, 2, 3],  # Noviembre, Diciembre, Enero, Febrero, Marzo
        'Año': [2024, 2024, 2025, 2025, 2025]
    })
    future_data['Precio_Media_3M'] = [df['Precio_Media_3M'].iloc[-1]] * len(future_data)
    future_data['Precio_Variacion'] = [df['Precio_Variacion'].iloc[-1]] * len(future_data)

    # Predicciones
    future_prices = model.predict(future_data)
    future_data['Precio m2'] = future_prices
    future_data['Mes'] = pd.to_datetime(
        [f"{month}-{year}" for month, year in zip(future_data['Mes_Num'], future_data['Año'])],
        format='%m-%Y'
    )

    # Graficar datos históricos y predicciones
    plt.figure(figsize=(10, 6))
    plt.plot(df['Mes'], df['Precio m2'], label="Histórico", marker='o')
    plt.plot(future_data['Mes'], future_data['Precio m2'], label="Predicción", marker='x', linestyle='--', color='red')
    plt.title(f"Evolución del Precio m2 - {barrio}")
    plt.xlabel("Mes")
    plt.ylabel("Precio m2 (€)")
    plt.legend()
    plt.grid()

    return plt  # Devuelve el gráfico para mostrarlo en Streamlit