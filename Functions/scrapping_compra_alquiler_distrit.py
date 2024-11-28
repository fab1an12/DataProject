from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import os
import random
import pandas as pd
import numpy as np
import undetected_chromedriver as uc


# Configuración de Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
browser = uc.Chrome()

# Lista de barrios que deseas procesar
busquedas = ["l-eixample", "l-olivereta", "patraix", "poblats-maritims", "quatre-carreres", "rascanya"]

# Tipos de transacciones
tipos = ["venta"]

# Crear un DataFrame global para almacenar todos los datos
df_total = pd.DataFrame()

# Iterar sobre cada tipo de transacción y barrio
for tipo in tipos:
    for busqueda in busquedas:
        print(f"\nProcesando {tipo} en el barrio: {busqueda}")
        
        busqueda = busqueda.replace(' ', '-')
        
        x = 1
        ids = []

        while True:
            url = f'https://www.idealista.com/{tipo}-viviendas/valencia/{busqueda}/pagina-{x}.htm'
            
            browser.get(url)
            
            time.sleep(random.randint(10, 12))
            
            try:
                browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
            except:
                pass
            
            html = browser.page_source
            
            soup = bs(html, 'lxml')
            
            # Verificar si estamos en la última página
            try:
                pagina_actual = int(soup.find('main', {'class': 'listing-items'})
                                        .find('div', {'class': 'pagination'})
                                        .find('li', {'class': 'selected'}).text)
            except AttributeError:
                print("No se encontraron más páginas para este barrio.")
                break
            
            if x == pagina_actual:
                articles = soup.find('main', {'class': 'listing-items'}).find_all('article')
            else:
                break
            
            x += 1
            
            for article in articles:
                id_muebles = article.get('data-element-id')
                ids.append(id_muebles)
                time.sleep(random.randint(1, 3))
                print(id_muebles)
            
            ids = [muebles for muebles in ids if muebles is not None]

        ids_casas = pd.DataFrame(ids, columns=['id'])
        print(ids_casas)

        casas = pd.Series()

        def parsear_inmueble(id_inmueble):
            print('\nCasa número: ' + id_inmueble)
            
            url = "https://www.idealista.com/inmueble/" + id_inmueble + "/"
            
            browser.get(url)
            
            html = browser.page_source
            soup = bs(html, 'lxml')

            titulo = soup.find('span', {'class': 'main-info__title-main'}).text
            print('\nTítulo: ' + titulo)
            
            localizacion = soup.find('span', {'class': 'main-info__title-minor'}).text.split(',')[0]
            print('\nLocalización: ' + localizacion)
            
            precio = int(soup.find('span', {'class': 'txt-bold'}).text.replace('.', ''))
            
            casas['titulo'] = titulo
            casas['localizacion'] = localizacion
            casas['precio'] = precio
            casas['tipo'] = tipo
            
            df_casas = pd.DataFrame(casas)
            return df_casas.T

        # Procesar cada inmueble
        df_casas = parsear_inmueble(ids_casas.iloc[0].id)

        for i in range(1, len(ids)):
            df_casas = pd.concat([df_casas, parsear_inmueble(ids[i])])
            time.sleep(random.randint(4, 8))
        
        print(df_casas)

        # Guardar datos del barrio y tipo actual
        ruta_guardado = os.path.join("DataProject", "Data", "Cost", "Ventas")
        if not os.path.exists(ruta_guardado):
            os.makedirs(ruta_guardado)
        
        archivo_casas = os.path.join(ruta_guardado, f'{busqueda}_{tipo}_idealista.csv')
        df_casas.to_csv(archivo_casas, index=False, sep=';', encoding='utf-16')
        print(f"Archivo guardado: {archivo_casas}")

