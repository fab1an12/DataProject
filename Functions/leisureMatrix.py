import numpy as np
import pandas as pd
from querys import obtener_ocio

def calcular_matriz_ahp_ocio():
    # Obtener los datos desde la consulta
    df = obtener_ocio()
    numero_ocio = df["total_ocio"].values
    n = len(numero_ocio)
    
    # Crear la matriz de comparación
    matriz_comparacion = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            matriz_comparacion[i, j] = numero_ocio[i] / numero_ocio[j]  # Directamente proporcional
    
    # Normalizar la matriz
    matriz_normalizada = matriz_comparacion / matriz_comparacion.sum(axis=0)
    
    # Calcular los pesos (promedio de filas normalizadas)
    pesos = matriz_normalizada.mean(axis=1)
    
    # Crear un DataFrame con los nombres de los barrios y sus pesos
    df_pesos = pd.DataFrame({"Distrito": df["distrito"], "Peso": pesos})
    
    return df_pesos

# Ejemplo de uso
a = calcular_matriz_ahp_ocio()
print(a)