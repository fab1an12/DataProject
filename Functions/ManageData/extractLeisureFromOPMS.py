import requests
import pandas as pd
from extractDistrict import extraer_barrios_sql

def contar_ocio_en_barrios():
    """
    Toma una lista de diccionarios con nombres de barrios y sus coordenadas, 
    y devuelve un DataFrame con el número de parques en cada barrio.
    
    :param barrios_lista: Lista de diccionarios con los datos de barrios.
    :return: DataFrame con los nombres de barrios y el número de parques.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"  # URL del servicio de Overpass
    resultados = []
    barrios_lista = extraer_barrios_sql()
    for barrio in barrios_lista:
        nombre = barrio["nombre"]
        query = f"""
        [out:json][timeout:25];
        area[name="{nombre}"]->.searchArea;
        (
        node["shop" = "department_store"](area.searchArea);
        way["shop" = "department_store"](area.searchArea);
        node["shop" = "mall"](area.searchArea);
        way["shop" = "mall"](area.searchArea);
        node["amenity" = "cinema"](area.searchArea);
        way["amenity" = "cinema"](area.searchArea);
        node["amenity" = "theatre"](area.searchArea);
        way["amenity" = "theatre"](area.searchArea);
        node["amenity" = "restaurant"](area.searchArea);
        way["amenity" = "restaurant"](area.searchArea);
        node["amenity" = "bar"](area.searchArea);
        way["amenity" = "bar"](area.searchArea);
        node["leisure" = "sports_centre"](area.searchArea);
        way["leisure" = "sports_centre"](area.searchArea);
        node["amenity" = "casino"](area.searchArea);
        way["amenity" = "casino"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            # Realizar la solicitud a la API de Overpass
            response = requests.get(overpass_url, params={"data": query})
            response.raise_for_status()  # Verifica si la solicitud tuvo éxito
            
            data = response.json()
            ocio_count = sum(
                1
                for element in data.get("elements", [])
                if element.get("type") in ["node", "way"] and
                (
                    element.get("tags", {}).get("leisure") in ["park", "playground", "sports_centre"] or
                    element.get("tags", {}).get("amenity") in ["cinema", "theatre", "restaurant", "bar", "casino"] or
                    element.get("tags", {}).get("shop") in ["department_store", "mall"]
                )
            )
        except Exception as e:
            print(f"Error al procesar el barrio '{nombre}': {e}")
            ocio_count = None
        
        resultados.append({"Barrio": nombre, "NumeroOcio": ocio_count})
    
    # Convertir los resultados en un DataFrame
    df_resultados = pd.DataFrame(resultados)
    return df_resultados
