import numpy as np
import pandas as pd
from greenZonesMatrix import calcular_matriz_ahp_zonas_verdes
from publicServicesMatrix import calcular_matriz_ahp_servicios_publicos
from rentCostMatrix import calcular_matriz_ahp_coste_alquiler
from salesCostMatrix import calcular_matriz_ahp_coste_compra
from transportMatrix import calcular_matriz_ahp_transporte

def generar_pesos_criterios(
    c_tr,  # Costes vs Transporte
    c_sp,  # Costes vs Servicios Públicos
    c_zv,  # Costes vs Zonas Verdes
    tr_sp, # Transporte vs Servicios Públicos
    tr_zv, # Transporte vs Zonas Verdes
    sp_zv  # Servicios Públicos vs Zonas Verdes
):
    # Inicializar la matriz de comparación
    n = 4  # Número de criterios
    matriz = np.ones((n, n))
    
    # Asignar las comparaciones
    matriz[0, 1] = c_tr
    matriz[1, 0] = 1 / c_tr

    matriz[0, 2] = c_sp
    matriz[2, 0] = 1 / c_sp

    matriz[0, 3] = c_zv
    matriz[3, 0] = 1 / c_zv

    matriz[1, 2] = tr_sp
    matriz[2, 1] = 1 / tr_sp

    matriz[1, 3] = tr_zv
    matriz[3, 1] = 1 / tr_zv

    matriz[2, 3] = sp_zv
    matriz[3, 2] = 1 / sp_zv

    # Normalizar la matriz y calcular los pesos
    matriz_normalizada = matriz / matriz.sum(axis=0)
    pesos = matriz_normalizada.mean(axis=1)
    print(pesos)
    # Retornar los pesos
    return pesos

def calcular_barrio_ideal(
    modo_coste,  # "Compra" o "Alquiler"
    pesos_criterios  # Pesos calculados de los criterios
):
    """
    Calcula el barrio ideal según el método AHP.

    Args:
        modo_coste (str): Indica si se utiliza el criterio de "Compra" o "Alquiler" para los costes.
        pesos_criterios (list): Lista de pesos de los criterios en el orden [Coste, Transporte, Servicios Públicos, Ocio].

    Returns:
        pd.DataFrame: DataFrame ordenado con los barrios y sus puntuaciones finales.
    """
    # Obtener las matrices de los criterios
    if modo_coste == "Compra":
        matriz_costes = calcular_matriz_ahp_coste_compra()
    elif modo_coste == "Alquiler":
        matriz_costes = calcular_matriz_ahp_coste_alquiler()
    else:
        raise ValueError("El parámetro 'modo_coste' debe ser 'Compra' o 'Alquiler'.")

    matriz_transporte = calcular_matriz_ahp_transporte()
    matriz_servicios = calcular_matriz_ahp_servicios_publicos()
    matriz_zonas_verdes = calcular_matriz_ahp_zonas_verdes()

    # Combinar matrices con los pesos
    matrices = [
        matriz_costes["Peso"].values,
        matriz_transporte["Peso"].values,
        matriz_servicios["Peso"].values,
        matriz_zonas_verdes["Peso"].values
    ]

    # Ponderar las matrices y calcular puntuaciones finales
    puntuaciones_finales = sum(p * w for p, w in zip(matrices, pesos_criterios))

    # Crear un DataFrame con los resultados
    df_resultados = pd.DataFrame({
        "Distrito": matriz_costes["Distrito"],  # Usamos los nombres de los barrios de cualquier matriz
        "Puntuación": puntuaciones_finales
    }).sort_values(by="Puntuación", ascending=False)

    # Devolver el DataFrame ordenado
    return df_resultados

print(calcular_barrio_ideal("Alquiler",generar_pesos_criterios(4,5,9,1/4,4,3)))

